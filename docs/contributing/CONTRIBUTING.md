# Contributing to Surviving the Singularity

Thank you for your interest in contributing to the Surviving the Singularity project! This document provides guidelines and instructions for contributors.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Style](#code-style)
4. [Security Guidelines](#security-guidelines)
5. [Database Security](#database-security)
6. [Pull Request Process](#pull-request-process)
7. [Community Guidelines](#community-guidelines)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/survivingthesingularity.git`
3. Install dependencies: `npm install`
4. Create a branch for your feature: `git checkout -b feature/your-feature-name`

## Development Workflow

1. Make your changes
2. Test your changes locally: `npm run dev`
3. Commit your changes with a descriptive commit message
4. Push to your fork: `git push origin feature/your-feature-name`
5. Create a pull request

## Code Style

We follow a specific code style to maintain consistency throughout the project. Please refer to our [Style Guide](./STYLE_GUIDE.md) for detailed information.

Key points:
- Use consistent indentation (2 spaces)
- Follow the SvelteKit project structure
- Write clear, descriptive comments
- Use meaningful variable and function names

## Security Guidelines

Security is a top priority for this project. Please review our comprehensive [Security Guidelines](./SECURITY.md) before making any contributions.

Key points:
- Never commit sensitive information
- Follow secure coding practices
- Properly handle user data
- Report security vulnerabilities privately

## Database Security

When working with Supabase or any database-related features, please follow our [Supabase Security Guidelines](./SUPABASE_SECURITY.md). These guidelines are crucial for maintaining the security and privacy of user data.

Key points:
- Never commit SQL files or database credentials
- Use Row Level Security (RLS) for all tables
- Follow the principle of least privilege
- Clean up sensitive files after use

## Pull Request Process

1. Ensure your code follows our style guide
2. Update documentation if necessary
3. Make sure all tests pass
4. Get at least one code review from a maintainer
5. Once approved, a maintainer will merge your PR

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others when you can
- Focus on the problem, not the person
- Give credit where credit is due

Thank you for contributing to Surviving the Singularity! Your efforts help us build a better platform for everyone.