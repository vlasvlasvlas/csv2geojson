import csv
import json
import sys
import re

# This script reads a CSV file containing GeoJSON data and converts it to a GeoJSON file.
# The script expects the input CSV file to have a column named 'JSON' containing the GeoJSON data.
# The script cleans the JSON content by removing non-printable characters and control characters except common whitespace.
# The script then combines all the GeoJSON features from the input CSV file into a single GeoJSON file.
# The script is intended to be run from the command line and requires two arguments: the input CSV file and the output GeoJSON file.
# Usage: python script.py <input_csv_file> <output_geojson_file>


def clean_json(json_content):
    """
    Clean JSON content by removing non-printable characters and control characters except common whitespace.
    params:
    json_content: str, JSON content to clean
    """
    # Remove non-printable characters and control characters except common whitespace
    json_content = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", json_content)

    # Remove the character "•" and line breaks
    json_content = json_content.replace("•", "").replace("\n", " ").replace("\r", "")
    return json_content


def convert_csv_to_geojson(input_csv_file, output_geojson_file):
    """
    Convert a CSV file containing GeoJSON data to a GeoJSON file.
    params:
    input_csv_file: str, path to the input CSV file
    output_geojson_file: str, path to the output GeoJSON file
    """
    csv.field_size_limit(1000000)  # Ajusta el límite de tamaño de los campos CSV

    feature_collections = []

    with open(input_csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            json_content = row["JSON"]
            # Skip rows with excessive length CSV fields to avoid memory errors
            if len(json_content) > 1000000:
                print(f"Skipping row {row['IdProyecto']} due to excessive length.")
                continue

            json_content = clean_json(json_content)  # Limpia el contenido JSON

            try:
                # assure that the JSON content is properly formatted
                if not json_content.endswith("}"):
                    json_content += "}"
                json_data = json.loads(json_content)
                feature_collections.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for row: {row['IdProyecto']} - {e}")
                print("Faulty JSON content:", json_content)

    # Create a GeoJSON object with all the features
    geojson = {
        "type": "FeatureCollection",
        "features": [
            feature
            for collection in feature_collections
            for feature in collection["features"]
        ],
    }

    # Save the GeoJSON data to a file
    with open(output_geojson_file, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)

    print("Conversion completed and saved to", output_geojson_file)


# Check if the script is being run directly and call the conversion function
if __name__ == "__main__":
    # Check if the input CSV file and output GeoJSON file are provided as arguments to the script
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_csv_file> <output_geojson_file>")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_geojson_file = sys.argv[2]

    # Convert the CSV file to GeoJSON
    convert_csv_to_geojson(input_csv_file, output_geojson_file)
