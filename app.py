import streamlit as st
import requests
 
# Backend API URL (change this when switching to FastAPI)
# API_URL = "http://127.0.0.1:5000/items"
 
# docker run --name my-postgres-db -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
# # Backend API URL (change this when switching to FastAPI)
# API_URL = "http://127.0.0.1:8000/items"
 
API_URL = "http://127.0.0.1:5000/items"
 
 
# Fetch all items from the backend
def fetch_items():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching items: {response.status_code}")
    return []
 
# Fetch item by ID
def fetch_item_by_id(item_id):
    response = requests.get(f"{API_URL}/{item_id}")
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching item {item_id}: {response.status_code}")
    return None
 
# Create new item
def create_item(item_data):
    try:
        response = requests.post(API_URL, json=item_data)
        response.raise_for_status()  # This will throw an exception for 4xx/5xx errors
        st.success("Item created successfully!")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error creating item: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
 
 
# Update item by ID
def update_item(item_id, item_data):
    response = requests.put(f"{API_URL}/{item_id}", json=item_data)
    if response.status_code == 200:
        st.success(f"Item {item_id} updated successfully!")
    else:
        st.error(f"Error updating item: {response.status_code} - {response.text}")
 
 
# Delete item by ID
def delete_item(item_id):
    response = requests.delete(f"{API_URL}/{item_id}")
    if response.status_code == 200:
        st.success(f"Item {item_id} deleted successfully!")
    else:
        st.error(f"Error deleting item: {response.status_code}")
 
st.title("Streamlit Frontend for FastAPI")
# Streamlit UI
st.subheader("Fetch Items")
if st.button("Fetch All Items"):
    items = fetch_items()
    st.write(items)
 
st.subheader("Fetch Item by ID")
item_id = st.number_input("Item ID", min_value=1)
if st.button("Fetch Item"):
    item = fetch_item_by_id(item_id)
    st.write(item)
 
st.subheader("Create New Item")
with st.form("create_item_form"):
    new_id = st.number_input("ID", min_value=1)
    new_name = st.text_input("Name")
    new_description = st.text_input("Description")
    new_price = st.number_input("Price", min_value=0.0, step=0.1)
    new_available = st.checkbox("Available", value=True)
    create_submit = st.form_submit_button("Create Item")
 
    if create_submit:
        new_item = {
            "id": new_id,
            "name": new_name,
            "description": new_description,
            "price": new_price,
            "available": new_available
        }
        create_item(new_item)
 
st.subheader("Update Item")
with st.form("update_item_form"):
    update_id = st.number_input("Update ID", min_value=1)
    update_name = st.text_input("Update Name")
    update_description = st.text_input("Update Description")
    update_price = st.number_input("Update Price", min_value=0.0, step=0.1)
    update_available = st.checkbox("Update Available", value=True)
    update_submit = st.form_submit_button("Update Item")
 
    if update_submit:
        updated_item = {
            "id": update_id,  # Ensure ID is included for PUT request
            "name": update_name,
            "description": update_description,
            "price": update_price,
            "available": update_available
        }
        update_item(update_id, updated_item)
 
st.subheader("Delete Item")
delete_id = st.number_input("Delete ID", min_value=1)
if st.button("Delete Item"):
    delete_item(delete_id)