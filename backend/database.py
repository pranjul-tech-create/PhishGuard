import sqlite3
from datetime import datetime


DATABASE = "phishguard.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # Create investigations table if it does not exist
    # ---------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investigation_type TEXT NOT NULL,
            target TEXT NOT NULL,
            prediction TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()

    # ---------------------------------------------------------
    # Existing + URL evidence columns
    # ---------------------------------------------------------

    existing_columns = {
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(investigations)"
        ).fetchall()
    }

    new_columns = {
        # URL investigation evidence
        "ml_confidence": "REAL",
        "rule_score": "INTEGER",
        "rule_level": "TEXT",
        "rule_reasons": "TEXT",
        "url_features": "TEXT",

        # VirusTotal evidence
        "vt_available": "INTEGER",
        "vt_malicious": "INTEGER",
        "vt_suspicious": "INTEGER",
        "vt_harmless": "INTEGER",
        "vt_undetected": "INTEGER",
        "vt_message": "TEXT",

        # Final assessment
        "final_reasons": "TEXT",

        # -------------------------------------------------
        # Email investigation evidence
        # -------------------------------------------------

        "email_sender": "TEXT",
        "email_recipient": "TEXT",
        "email_subject": "TEXT",
        "email_date": "TEXT",
        "email_reply_to": "TEXT",
        "email_return_path": "TEXT",
        "email_suspicious_keywords": "TEXT",
        "email_attachments": "TEXT",
        "email_authentication_results": "TEXT",
        "email_received_headers": "TEXT",
        "email_urls": "TEXT",
        "email_reasons": "TEXT",
    }

    # ---------------------------------------------------------
    # Add missing columns automatically
    # ---------------------------------------------------------

    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE investigations
                ADD COLUMN {column_name} {column_type}
                """
            )

    connection.commit()
    connection.close()


def save_investigation(
    investigation_type,
    target,
    prediction,
    risk_score,
    risk_level,

    # URL fields
    ml_confidence=None,
    rule_score=None,
    rule_level=None,
    rule_reasons=None,
    url_features=None,

    # VirusTotal fields
    vt_available=None,
    vt_malicious=None,
    vt_suspicious=None,
    vt_harmless=None,
    vt_undetected=None,
    vt_message=None,

    # Final assessment
    final_reasons=None,

    # Email fields
    email_sender=None,
    email_recipient=None,
    email_subject=None,
    email_date=None,
    email_reply_to=None,
    email_return_path=None,
    email_suspicious_keywords=None,
    email_attachments=None,
    email_authentication_results=None,
    email_received_headers=None,
    email_urls=None,
    email_reasons=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO investigations
        (
            investigation_type,
            target,
            prediction,
            risk_score,
            risk_level,
            created_at,

            ml_confidence,
            rule_score,
            rule_level,
            rule_reasons,
            url_features,

            vt_available,
            vt_malicious,
            vt_suspicious,
            vt_harmless,
            vt_undetected,
            vt_message,

            final_reasons,

            email_sender,
            email_recipient,
            email_subject,
            email_date,
            email_reply_to,
            email_return_path,
            email_suspicious_keywords,
            email_attachments,
            email_authentication_results,
            email_received_headers,
            email_urls,
            email_reasons
        )

        VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        investigation_type,
        target,
        prediction,
        risk_score,
        risk_level,
        datetime.now().isoformat(),

        ml_confidence,
        rule_score,
        rule_level,
        rule_reasons,
        url_features,

        vt_available,
        vt_malicious,
        vt_suspicious,
        vt_harmless,
        vt_undetected,
        vt_message,

        final_reasons,

        email_sender,
        email_recipient,
        email_subject,
        email_date,
        email_reply_to,
        email_return_path,
        email_suspicious_keywords,
        email_attachments,
        email_authentication_results,
        email_received_headers,
        email_urls,
        email_reasons
    ))

    connection.commit()
    connection.close()


def get_investigations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM investigations
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_investigation_by_id(investigation_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM investigations
        WHERE id = ?
    """, (investigation_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)