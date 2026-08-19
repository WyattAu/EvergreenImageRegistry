use clap::Parser;

use evergreenctl::cli::{Cli, validate_command_paths};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let cli = Cli::parse();

    // Validate all path arguments for traversal attacks
    validate_command_paths(&cli.command)?;

    // Dispatch to the command handler
    evergreenctl::run::execute(cli.command).await
}
