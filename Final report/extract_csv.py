import pandas as pd
import requests
import os

# Define the file path and the column name containing the image links
file_path = '/Volumes/PC and Mac/Plant_net/data/multimedia.txt'  # Replace with your CSV file path
link_column = 'pictures_link'  # Replace with the actual column name containing the links
name_column = 'description'
save_directory = '/Volumes/PC and Mac/Plant_net/downloaded_images' # Directory to save downloaded images
output_csv = '/Volumes/PC and Mac/Plant_net/image_types.csv'  # Output CSV file to record types

# Create a directory to save the images if it doesn't already exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Define the chunk size
chunksize = 100  # Number of rows to read at a time
# Open the output CSV file in write mode


with open(output_csv, mode='w') as file:
    # Write the header row
    file.write('image_filename,type\n')
# Process the CSV file in chunks
    for chunk in pd.read_csv(file_path, delimiter='\t', chunksize=chunksize):
        # Loop over each row in the chunk
        for idx, row in chunk.iterrows():
            # Print the link in the specified column
            description = row[name_column]
            link = row[link_column]
            # Extract only the type part of the name
            type_name = description.split(":")[-1].strip() if ":" in description else description
            #if type == other skip the line
            if type_name.lower() == "other":
                continue
            if type_name.lower() == "branch":
                continue
            if type_name.lower() == "habit":
                continue

            # Define the filename for the image
            image_filename = f'image_{idx + 1}.jpg'
            image_path = os.path.join(save_directory, image_filename)

            try:
                # Download the image
                response = requests.get(link, stream=True)
                if response.status_code == 200:
                    # Save the image
                    with open(image_path, 'wb') as img_file:
                        for chunk in response.iter_content(1024):
                            img_file.write(chunk)
                    if idx % 1000 == 0:
                        print(f"Downloaded {image_path}")

                    # Write the type and image filename to the output CSV
                    file.write(f'{image_filename},{type_name}\n')
                else:
                    print(f"Failed to download image at index {idx}, status code {response.status_code}")
            except Exception as e:
                print(f"Error downloading image at index {idx}: {e}")

print("Download complete, and type data saved to CSV.")