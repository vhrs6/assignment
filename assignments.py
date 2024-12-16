import streamlit as st
from PIL import Image
import os
import random
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Set the page configuration
st.set_page_config(page_title="Biocon Biologics", page_icon="📄", layout="wide")

# Define the users and passwords (for simplicity, it's hardcoded)
correct_username = "Nithin"
correct_password = "nithin@2111"

# Check if the user is authenticated via session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Display login page if not authenticated
if not st.session_state.authenticated:
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        if username_input == correct_username and password_input == correct_password:
            st.session_state.authenticated = True
            st.session_state.username = username_input
            st.success(f"Welcome {username_input}!")
        else:
            st.error("Invalid username or password. Please try again.")

else:
    # User is authenticated, show the app
    st.title("📄 Biocon Biologics Portal")
    st.write(
        f"Welcome back, {st.session_state.username}! Use this portal to upload and manage your files."
    )

    # Generate fake data till 10 December 2024
    def generate_fake_data():
        data = []
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime(2024, 12, 10)
        current_date = start_date

        while current_date <= end_date:
            assign_date = current_date
            # Randomly decide if submission is completed
            if random.random() < 0.7:  # 70% chance of submission
                submission_date = assign_date + timedelta(days=random.randint(1, 5))
                num_assignments = random.randint(1, 5)
            else:  # Leave some entries incomplete
                submission_date = None
                num_assignments = None

            data.append(
                {
                    "Date of Assignment": assign_date.strftime("%Y-%m-%d"),
                    "Date of Submission": (
                        submission_date.strftime("%Y-%m-%d") if submission_date else ""
                    ),
                    "Files Submitted": num_assignments,
                    "Completed": bool(
                        submission_date
                    ),  # Mark as completed if submitted
                }
            )
            current_date += timedelta(days=1)
        return pd.DataFrame(data)

    # Generate and display fake data
    dataframe = generate_fake_data()

    # Generate fake metrics
    def generate_fake_metrics(data):
        total_assignments = (
            data["Files Submitted"].fillna(0).sum()
        )  # Count only submitted assignments
        total_credits = total_assignments * 10  # Assuming each file earns 10 credits
        return int(total_assignments), total_credits

    total_assignments, total_credits = generate_fake_metrics(dataframe)

    # Sidebar for user profile and logo
    with st.sidebar:
        # Logo at the top using st.logo
        try:
            st.logo("download.png")  # Display the 'download.png' logo using st.logo
        except FileNotFoundError:
            st.warning(
                "Logo image 'download.png' not found. Please ensure it's in the app directory."
            )

        st.markdown("Biocon Biologics ®")  # Separator for clean layout
        st.markdown("---")  # Separator for clean layout

        # User Profile Section
        st.markdown("### User Profile")

        # Displaying user profile picture (smaller size)
        try:
            user_img = Image.open("d.jpg")  # Load predefined image
            st.image(
                user_img, caption="Nithin Jois", use_container_width=True, width=100
            )  # Small image with width adjustment
        except FileNotFoundError:
            st.image(
                "https://via.placeholder.com/150",
                caption="Default Profile Picture",
                use_container_width=True,
                width=100,
            )
            st.warning(
                "Profile picture not found. Please ensure 'n.png' is in the app directory."
            )

        # Displaying user details below the picture
        st.markdown("#### **Nithin Jois**")
        st.markdown(
            """
        **Age:** 25 years  
        **Location:** Bengaluru, Karnataka, India
        """
        )

        # Add a personalized welcome message
        st.markdown("### Welcome, Nithin!")
        st.markdown("You are doing great. Keep up the good work! 🚀")

        # Add progress bar stuck at 25%
        completed_percentage = 25  # Set the progress bar to 25%
        st.markdown("### Your Progress")
        st.progress(completed_percentage)  # Show the progress bar

        # Navigation Links for different sections
        st.markdown("### Navigation")
        st.markdown("[Upload Assignments](#upload-your-files)")
        st.markdown("[View Metrics](#current-metrics)")

        # Add a recent activities section (e.g., recent uploads)
        st.markdown("### Recent Activity")
        if os.path.exists("uploaded_assignments"):
            files = os.listdir("uploaded_assignments")
            if files:
                st.write("You uploaded the following files recently:")
                for file in files[-3:]:  # Show the last 3 uploaded files
                    st.markdown(f"- {file}")
            else:
                st.write("No files uploaded yet.")
        else:
            st.write("No files uploaded yet.")

        # Add Company Info Section
        st.markdown("### About Biocon Biologics ®")
        st.write(
            """
        **Biocon Biologics** is a fully integrated global player in biologics and one of the largest manufacturers of biosimilars in the world. 
        We are committed to improving patient access to life-saving biologics by driving innovation and excellence in manufacturing. 
        Our products are available in over 60 countries worldwide.
        """
        )

    # Main interface
    # st.title("📄 Biocon Biologics Portal")
    # st.write("Welcome! Use this portal to upload and manage your files and view metrics.")

    # Metrics section
    st.markdown("---")
    st.markdown("### 📊 Current Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Files Submitted", total_assignments)
    with col2:
        st.metric("Total Credits Earned", total_credits)
    st.markdown("---")

    # File uploader for assignments
    st.header("Upload Your Files")
    uploaded_file = st.file_uploader(
        "Choose a file to upload", type=["pdf", "docx", "txt"]
    )
    if uploaded_file:
        save_path = os.path.join("uploaded_assignments", uploaded_file.name)
        os.makedirs("uploaded_assignments", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"'{uploaded_file.name}' uploaded successfully!")
        st.write("Saved to:", save_path)

        # Update metrics dynamically
        st.info(
            "Note: Uploaded files are currently not linked to the table metrics dynamically."
        )

    # Display uploaded files
    st.header("Uploaded Files")
    if os.path.exists("uploaded_assignments"):
        files = os.listdir("uploaded_assignments")
        if files:
            for file in files:
                st.markdown(f"- {file}")
        else:
            st.write("No files uploaded yet.")
    else:
        st.write("No files uploaded yet.")

    # Display fake data
    st.markdown("### 📅 Monthly Submission Data")
    dataframe.index += 1  # Start index from 1
    st.dataframe(dataframe, use_container_width=True)

    # Calculate performance for Donut Chart and Line Chart
    completed_assignments = dataframe["Completed"].sum()
    incomplete_assignments = len(dataframe) - completed_assignments

    # Create Donut Chart
    performance_data = {
        "Category": ["Completed", "Incomplete"],
        "Count": [completed_assignments, incomplete_assignments],
    }

    # Create Plotly donut chart
    fig_donut = px.pie(
        performance_data,
        names="Category",
        values="Count",
        hole=0.4,
        title="User Performance",
    )

    # Line Chart to show efficiency over time
    efficiency_data = []
    for index, row in dataframe.iterrows():
        total_assignments_for_day = (
            row["Files Submitted"] if row["Files Submitted"] is not None else 0
        )
        completed_assignments_for_day = (
            row["Completed"] * row["Files Submitted"] if row["Completed"] else 0
        )
        efficiency = (
            completed_assignments_for_day / total_assignments_for_day
            if total_assignments_for_day > 0
            else 0
        )
        efficiency_data.append(
            {"Date": row["Date of Assignment"], "Efficiency": efficiency}
        )

    # Create efficiency dataframe
    efficiency_df = pd.DataFrame(efficiency_data)

    # Create Line Chart for Efficiency
    fig_line = go.Figure()
    fig_line.add_trace(
        go.Scatter(
            x=efficiency_df["Date"],
            y=efficiency_df["Efficiency"],
            mode="lines",
            name="Efficiency",
        )
    )

    # Show charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)

    st.caption("Biocon Biologics ®")
