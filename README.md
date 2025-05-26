# Phase-3-Code-Challenge

#  Articles Domain Modeling with SQL (Without SQLAlchemy)

## Overview

This project models the relationships between **Authors**, **Articles**, and **Magazines** using **Python OOP** and **raw SQL** (no ORM). It simulates a publishing platform where:

- An **Author** can write multiple Articles
- A **Magazine** can publish multiple Articles
- An **Article** belongs to one Author and one Magazine

> This project satisfies the **Phase 3 Code Challenge** requirements for Moringa School Software Engineering Program.

---

## 🗂️ Project Structure

code challange/
│
├── lib/
│ ├── db/
│ │ ├── connection.py # Database connection
│ │ ├── schema.sql # SQL schema definitions
│ │ └── seed.py # Optional seed data
│ │
│ ├── models/
│ │ ├── init.py # Models module initializer
│ │ ├── author.py # Author model
│ │ ├── article.py # Article model
│ │ └── magazine.py # Magazine model
│ │
│ ├── debug.py # Interactive testing console
│ └── init.py # Lib package initializer
│
├── scripts/
│ ├── setup_db.py # Run schema & initialize DB
│ └── run_queries.py # Optional query tests
│
├── tests/
│ ├── test_author.py # Tests for Author
│ ├── test_article.py # Tests for Article
│ └── test_magazine.py # Tests for Magazine
│
├── articles.db # SQLite3 database file (auto-generated)
└── README.md #

## 🧰 Technologies Used

- **Python 3.10+**
- **SQLite3** for relational database
- **Pytest** for unit testing
- **Raw SQL queries** (no SQLAlchemy or ORM)

---

## 🔧 Setup Instructions

1. **Clone the repo**

git clone [https://github.com/your-username/articles-code-challenge.git](https://github.com/ezraoduor/Phase-3-Code-Challenge)
cd articles-code-challenge

Set up environment

Using venv:

python -m venv env
source env/bin/activate  # or `.\env\Scripts\activate` on Windows
pip install -r requirements.txt


 ## Features
 # Author
save(), find_by_id(), find_by_name()

articles(), magazines()

add_article(title, magazine)

topic_areas()

# Magazine
save(), find_by_id(), find_by_name()

articles(), contributors(), article_titles(), contributing_authors()

# Article
save(), find_by_id(), find_by_title()

Links between Author and Magazine

# Testing
All core methods tested using pytest

Tests are located in the tests/ directory

# Deliverables Checklist
 Author, Article, Magazine classes with SQL methods

 Correct relationships and foreign keys

 Schema: authors, articles, magazines

 Relationship queries and validations

 Transaction handling (e.g. add_author_with_articles)

 Passes all tests with pytest

 Git commits are structured and descriptive

# Bonus (if implemented)
 Magazine.top_publisher() — get magazine with most articles

 Add DB indexes

 CLI tool for interactive querying

