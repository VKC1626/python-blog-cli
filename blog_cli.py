from dotenv import load_dotenv
import os

load_dotenv()

import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cursor = conn.cursor()


def create_post(title, content, tag_list):
    cursor.execute(
        "INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content)
    )
    post_id = cursor.lastrowid

    for tag_name in tag_list:
        cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
        tag = cursor.fetchone()
        if not tag:
            cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag_name,))
            tag_id = cursor.lastrowid
        else:
            tag_id = tag[0]
        cursor.execute(
            "INSERT IGNORE INTO post_tags (post_id, tag_id) VALUES (%s, %s)",
            (post_id, tag_id),
        )

    conn.commit()
    print("Post created successfully.")


def view_all_titles():
    cursor.execute("SELECT title FROM posts")
    results = cursor.fetchall()
    if results:
        print("\n All Post Titles:")
        for (title,) in results:
            print("- " + title)
    else:
        print("No posts found.")


def view_post_by_title(title):
    cursor.execute("SELECT content FROM posts WHERE title = %s", (title,))
    post = cursor.fetchone()
    if post:
        print(f"\n {title}\n{'-' * len(title)}\n{post[0]}")
    else:
        print("Post not found.")


def search_by_tag(tag_name):
    query = """
        SELECT p.title
        FROM posts p
        JOIN post_tags pt ON p.id = pt.post_id
        JOIN tags t ON t.id = pt.tag_id
        WHERE t.name = %s
    """
    cursor.execute(query, (tag_name,))
    results = cursor.fetchall()
    if results:
        print(f"\n Posts with tag '{tag_name}':")
        for (title,) in results:
            print("- " + title)
    else:
        print("No posts found with that tag.")


def menu():
    while True:
        print("\n Blog CLI Menu")
        print("1. Create new post")
        print("2. View all post titles")
        print("3. View post by title")
        print("4. Search posts by tag")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            title = input("Enter post title: ")
            content = input("Enter post content: ")
            tags = input("Enter comma-separated tags: ").split(",")
            tag_list = [tag.strip() for tag in tags]
            create_post(title, content, tag_list)

        elif choice == "2":
            view_all_titles()

        elif choice == "3":
            title = input("Enter title to view: ")
            view_post_by_title(title)

        elif choice == "4":
            tag = input("Enter tag to search: ")
            search_by_tag(tag)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


menu()
