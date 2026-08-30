// =============================================================================
// Evergreenctl - Output Formatting Utilities
// =============================================================================
// Eliminates repeated `match format.as_str()` blocks across the codebase.
// Provides generic functions for serializing results to JSON or text.
// =============================================================================

use anyhow::Result;
use serde::Serialize;

/// Output format options.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutputFormat {
    Json,
    Text,
    Tsv,
}

impl OutputFormat {
    /// Parse from a string, defaulting to Text.
    pub fn parse(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "json" => OutputFormat::Json,
            "tsv" => OutputFormat::Tsv,
            _ => OutputFormat::Text,
        }
    }
}

/// Output a serializable result in the specified format.
///
/// # Arguments
/// * `data` - The data to serialize
/// * `format` - The output format (json, text, tsv)
/// * `text_fn` - Function to convert data to human-readable text
pub fn output_result<T: Serialize>(
    data: &T,
    format: &str,
    text_fn: impl Fn(&T) -> String,
) -> Result<()> {
    let fmt = OutputFormat::parse(format);
    match fmt {
        OutputFormat::Json => {
            println!("{}", serde_json::to_string_pretty(data)?);
        }
        _ => {
            println!("{}", text_fn(data));
        }
    }
    Ok(())
}

/// Output a serializable result, returning the formatted string instead of printing.
pub fn format_result<T: Serialize>(
    data: &T,
    format: &str,
    text_fn: impl Fn(&T) -> String,
) -> Result<String> {
    let fmt = OutputFormat::parse(format);
    match fmt {
        OutputFormat::Json => Ok(serde_json::to_string_pretty(data)?),
        _ => Ok(text_fn(data)),
    }
}

/// Output a simple message with optional exit code.
pub fn output_message(message: &str, format: &str) -> Result<()> {
    let fmt = OutputFormat::parse(format);
    match fmt {
        OutputFormat::Json => {
            println!("{}", serde_json::json!({"message": message}));
        }
        _ => {
            println!("{}", message);
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde::Serialize;

    #[derive(Serialize)]
    struct TestData {
        name: String,
        count: usize,
    }

    #[test]
    fn test_output_format_parse() {
        assert_eq!(OutputFormat::parse("json"), OutputFormat::Json);
        assert_eq!(OutputFormat::parse("JSON"), OutputFormat::Json);
        assert_eq!(OutputFormat::parse("text"), OutputFormat::Text);
        assert_eq!(OutputFormat::parse("tsv"), OutputFormat::Tsv);
        assert_eq!(OutputFormat::parse("unknown"), OutputFormat::Text);
    }

    #[test]
    fn test_format_result_json() {
        let data = TestData {
            name: "test".into(),
            count: 42,
        };
        let result = format_result(&data, "json", |d| format!("{}: {}", d.name, d.count)).unwrap();
        assert!(result.contains("\"name\": \"test\""));
        assert!(result.contains("42"));
    }

    #[test]
    fn test_format_result_text() {
        let data = TestData {
            name: "test".into(),
            count: 42,
        };
        let result = format_result(&data, "text", |d| format!("{}: {}", d.name, d.count)).unwrap();
        assert_eq!(result, "test: 42");
    }

    #[test]
    fn test_format_result_tsv_uses_text() {
        let data = TestData {
            name: "test".into(),
            count: 42,
        };
        // TSV falls through to the text branch
        let result = format_result(&data, "tsv", |d| format!("{}: {}", d.name, d.count)).unwrap();
        assert_eq!(result, "test: 42");
    }

    #[test]
    fn test_format_result_unknown_format() {
        let data = TestData {
            name: "test".into(),
            count: 1,
        };
        // Unknown format defaults to text
        let result = format_result(&data, "xml", |d| d.name.to_string()).unwrap();
        assert_eq!(result, "test");
    }
}
