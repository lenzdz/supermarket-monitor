> [!TIP]
> This README is written in English. You can read the Spanish version by following [this link](README.md).

# Supermarket Monitor

**Supermarket Monitor** is a Python application that automatically monitors product prices from Colombian supermarkets and pharmacies, detects discounts, and sends Discord notifications whenever relevant deals are found.

It currently integrates Olímpica, Jumbo, Cruz Verde, Makro, and Farmatodo, and was designed to make it easy to add support for new retail chains in the future.

## Features

- Automatically retrieves product prices from each store's API (except Cruz Verde, which is scraped using Playwright).
- Detects both general discounts and exclusive promotions (such as membership clubs or credit card offers).
- Compares prices for equivalent products across different retailers.
- Automatically sends notifications to Discord channels.
- Modular architecture that simplifies the integration of new supermarkets and pharmacies.
- Compatible with scheduled execution through GitHub Actions.

## Project Structure

```
olimpica-monitor/

│

├── scraper/          # API clients for each retailer

├── services/         # Monitoring and price comparison logic

├── notifiers/        # Discord notification handlers

├── data/             # Product database stored as JSON

├── main.py           # Application entry point

└── requirements.txt
```

## Supported Stores

🛒 Olímpica

🛒 Jumbo

🛒 Makro

💊 Cruz Verde

💊 Farmatodo

## How It Works

Each retailer has an independent client responsible for querying its API or website and normalizing the retrieved information.

The monitoring services iterate through the product lists defined in the JSON files, fetch the latest prices, and generate a standardized data structure containing information such as the product name, regular price, current price, and promotional price (when available). Currently, the product database is maintained manually because the project is intended to monitor only a selected set of products rather than every item sold by each retailer.

Next, the application determines whether the product is currently on sale, compares its price with equivalent products from other retailers whenever available, and sends a Discord notification if appropriate.

Equivalent products can be mapped through a configuration file (`productos_comparables.json`).

This allows the system not only to report a discount, but also to indicate when the same product is available at a lower price from another retailer.

### Example

![Screenshot showing the Cruz Verde execution output of the Supermarket Monitor project](img/funcionamiento-cruzverde.png)

## Technologies Used

- Python 3
- Requests
- Playwright (when session-protected information must be retrieved)
- Beautiful Soup
- Discord Webhooks
- GitHub Actions

## Automation

The project is designed to run on a schedule using GitHub Actions, allowing product prices to be checked multiple times a day without the need to maintain a dedicated server.

## Purpose

The goal of this project is to build a scalable price monitoring platform that helps users identify savings opportunities and compare offers across different Colombian supermarkets and pharmacies, while providing an architecture that makes it easy to integrate additional retailers in the future.
