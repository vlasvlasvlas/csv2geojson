# CSV to GeoJSON Converter

This Python script converts CSV files containing JSON strings in a specific column into well-formatted GeoJSON files. It includes functionality to handle large JSON fields and cleans up JSON strings to ensure they are free from control characters and other common formatting issues.

## Features

- **Extracts JSON strings** from a specified column in the CSV.
- **Cleans JSON format** by removing control characters and unwanted special characters.
- **Converts multiple JSON FeatureCollections** into a single GeoJSON file.
- **Skips rows with excessively large JSON fields** to prevent overflow errors and ensure efficient processing.
- **Handles invalid control characters** in JSON strings to ensure valid JSON formatting.

## Requirements

- **Python 3.x**: Ensure Python 3 is installed on your machine.
- **Standard Python libraries**: Uses `csv`, `json`, `sys`, and `re`, which are included in standard Python installations.

## Usage

Run the script from the command line by specifying the input CSV file and the output GeoJSON file as arguments:

```bash
python script.py <input_csv_file> <output_geojson_file>
```

## Input File Format

The input CSV file should have at least the following columns:
- `IdProyecto`: Unique identifier for each project.
- `JSON`: Column containing JSON strings that represent individual GeoJSON FeatureCollections.

## Output File

The output is a single GeoJSON file that combines all features from the processed JSON strings into one FeatureCollection.

## Example

```bash
python script.py dataset_in.csv dataset_out.geojson
```

This will read `dataset_in.csv`, process the JSON content, and output a valid GeoJSON to `dataset_out.geojson`.

## Function Descriptions

- **`clean_json(json_content)`**: This function removes non-printable and control characters, unwanted special characters like "•", and newline characters from JSON strings, ensuring that the JSON can be correctly parsed.

## Handling Large and Faulty Data

- The script automatically skips rows where the JSON string exceeds a predefined size limit (e.g., 1,000,000 characters) to avoid `OverflowError`.
- It also corrects and cleans up JSON strings, which could otherwise cause parsing errors due to format issues such as invalid control characters.

## Contributing

Contributions to improve the script or handle additional edge cases are welcome. Feel free to fork this project and submit a pull request.

## License

This project is open-source and available under the MIT License.
