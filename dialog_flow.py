import pandas as pd
from diagrams import Diagram
from diagrams.aws.general import General
from PIL import Image
import os
import matplotlib.pyplot as plt

# Load Excel or CSV file
def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    return data

# Generate flowchart
def create_flowchart(data, output_file="job_flowchart"):
    with Diagram(output_file, show=False):
        job_nodes = {}

        # Create a General box icon for each jobname
        for index, row in data.iterrows():
            job_ref = row['jobname_referencia']
            job_pred = row['jobname_predecessor']
            job_succ = row['jobname_sucessor']
            
            # Create or get the reference job node
            if job_ref not in job_nodes:
                job_nodes[job_ref] = General(job_ref)

            # Create or get the predecessor job node
            if pd.notna(job_pred) and job_pred not in job_nodes:
                job_nodes[job_pred] = General(job_pred)
                job_nodes[job_pred] >> job_nodes[job_ref]  # Predecessor to reference

            # Create or get the successor job node
            if pd.notna(job_succ) and job_succ not in job_nodes:
                job_nodes[job_succ] = General(job_succ)
                job_nodes[job_ref] >> job_nodes[job_succ]  # Reference to successor

# Function to display the flowchart as a modal (pop-up window)
def display_flowchart(output_file="job_flowchart"):
    # Load the image using PIL
    img = Image.open(output_file + ".png")
    
    # Display the image using matplotlib in a pop-up modal window
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis('off')  # Hide axes
    plt.show()  # Display the modal window with the flowchart

# Main function
if __name__ == "__main__":
    # Provide the path to your Excel or CSV file
    file_path = "jobs_data.xlsx"

    # Load the data
    data = load_data(file_path)

    if data is not None:
        # Create the flowchart and save as PNG
        create_flowchart(data)
        print("Flowchart created successfully.")

        # Display the flowchart in a modal
        display_flowchart("job_flowchart")
