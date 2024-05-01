from dotenv import load_dotenv
import mysql.connector
import streamlit as st
import os
import google.generativeai as genai


load_dotenv()  # load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))  # Configure Gemini api key

def get_gemini_response(user_text, ai_prompt):

    """
    :param user_text: user question from the frontend in the form of text
    :param ai_prompt: text we use to prompt Gemini
    :return: gemini SQL query
    """

    model = genai.GenerativeModel('gemini-pro')
    ai_response = model.generate_content([ai_prompt[0], user_text])
    return ai_response.text


def read_sql_query(sql_query):

    """
    :param sql_query: SQL query to query the db
    :return: queried data rows
    """

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cur = conn.cursor()
    cur.execute(sql_query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


# defining our prompt
prompt = [
    """
    You are an expert in SQL queries!

    The SQL database contains the following tables:

    Table 1: user
    Columns: id (BINARY(16) NOT NULL UNIQUE), password_hash (VARCHAR(64)), first_name (VARCHAR(64)), last_name (VARCHAR(64)), email (VARCHAR(30) UNIQUE), phone_number (VARCHAR(15) UNIQUE), image_url (VARCHAR(256)), activated (BIT NOT NULL), user_type (VARCHAR(11) NOT NULL), created_by (VARCHAR(255)), creation_date (DATETIME), last_modified_by (VARCHAR(255)), last_modified_date (DATETIME)

    Table 2: authority
    Columns: id (BINARY(16) NOT NULL UNIQUE), authority_name (VARCHAR(64) NOT NULL), created_by (VARCHAR(255)), creation_date (DATETIME), last_modified_by (VARCHAR(255)), last_modified_date (DATETIME)

    Table 3: user_authority
    Columns: user_id (BINARY(16) NOT NULL), authority_id (BINARY(16) NOT NULL)

    Table 4: currency
    Columns: id (BINARY(16) NOT NULL UNIQUE), name (VARCHAR(64) NOT NULL), symbol (VARCHAR(30) NOT NULL UNIQUE), enabled (BIT NOT NULL), created_by (VARCHAR(255)), creation_date (DATETIME), last_modified_by (VARCHAR(255)), last_modified_date (DATETIME)

    Table 5: transactions
    Columns: id (BINARY(16) NOT NULL UNIQUE), amount (DECIMAL(64) NOT NULL), type (VARCHAR(15) NOT NULL), purpose (VARCHAR(35) NOT NULL), account_id (BINARY(16) NOT NULL), reference (BINARY(16) NOT NULL UNIQUE), status (VARCHAR(30) NOT NULL), description (VARCHAR(255)), sender_account (VARCHAR(20) NOT NULL), receiver_account (VARCHAR(20) NOT NULL), created_by (VARCHAR(255)), creation_date (DATETIME), last_modified_by (VARCHAR(255)), last_modified_date (DATETIME)

    Table 6: account
    Columns: id (BINARY(16) NOT NULL UNIQUE), available_balance (DECIMAL(64) NOT NULL), reserved_balance (VARCHAR(30) NOT NULL), locked (BIT NOT NULL), status (VARCHAR(20) NOT NULL), type (VARCHAR(20) NOT NULL), currency_id (BINARY(16) NOT NULL), user_id (BINARY(16) NOT NULL), account_number (VARCHAR(20) NOT NULL UNIQUE), created_by (VARCHAR(255)), creation_date (DATETIME), last_modified_by (VARCHAR(255)), last_modified_date (DATETIME)
    Please provide an English question related to these tables, and I'll help you generate the corresponding SQL query.
    also the sql code should not have ``` in beginning or end and sql word in output
    """

]

# Creating a streamlit app
st.set_page_config(page_title="Query Databases with Gemini Pro")
st.header("Gemini App To Retrieve Data With Normal Text")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
try:
    if submit:
        response = get_gemini_response(question, prompt)
        print(response)
        response = read_sql_query(response)
        st.subheader("The Response is")
        for row in response:
            print(row)
            st.header(row)

except Exception as exception:
    st.header("could not generate query from your input")
