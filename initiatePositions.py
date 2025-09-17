import numpy as np

def convert_to_full_coordinates(molecule_data: dict, y_center: float, z_center: float) -> dict:
    """
    Converts a dictionary of molecule coordinates to full 3D coordinates.

    This function iterates through a dictionary where keys are molecule names
    and values are lists of coordinates. It checks each coordinate list and
    pads it with zeros to ensure it has three dimensions (x, y, z).

    - [x] becomes [x, y_center, z_center]
    - [x, y] becomes [x, y, z_center]
    - [x, y, z] remains unchanged

    Args:
        molecule_data: A dictionary with molecule names as keys and lists
                       of coordinates as values.

    Returns:
        A new dictionary with all coordinates converted to [x, y, z] format.
        
    # Example Usage:
    # Define a sample input dictionary with mixed coordinate formats
    sample_input = {
        "water": [
            [0.1],          # Only x is provided
            [0.9, 0.5],     # x and y are provided
            [-0.5, -0.5, 0.1] # Full x, y, z
        ],
        "ammonia": [
            [1.0],
            [1.5, 2.0],
            [2.0, 2.0, 2.5]
        ]
    }

    # Convert the coordinates
    full_coordinates_data = convert_to_full_coordinates(sample_input, 10, 10)
    print("Original Data:")
    print(sample_input)
    print("\nConverted Data:")
    print(full_coordinates_data)
    
    # Expected Output:
    # Original Data:
    # {'water': [[0.1], [0.9, 0.5], [-0.5, -0.5, 0.1]], 'ammonia': [[1.0], [1.5, 2.0], [2.0, 2.0, 2.5]]}
    #
    # Converted Data:
    # {'water': [[0.1, 0, 0], [0.9, 0.5, 0], [-0.5, -0.5, 0.1]], 'ammonia': [[1.0, 10, 10], [1.5, 2.0, 10], [2.0, 2.0, 2.5]]}
    """
    # Create a new dictionary to store the processed data to avoid modifying the original
    processed_data = {}

    # Iterate over each molecule and its list of coordinates in the input dictionary
    for molecule_name, coordinates_list in molecule_data.items():
        full_coordinates = []
        # Iterate over each coordinate point for the current molecule
        for coords in coordinates_list:
            # Create a copy to avoid modifying the original sub-list
            full_coord = list(coords)
            # Check the length of the coordinate list and pad with zeros if necessary
            if len(full_coord) == 1:
                full_coord.extend([y_center, z_center])  # Append y and z
            elif len(full_coord) == 2:
                full_coord.append(z_center)  # Append z
            # Add the full coordinate to our list for this molecule
            full_coordinates.append(full_coord)
        # Add the processed list of coordinates to our new dictionary
        processed_data[molecule_name] = full_coordinates

    return processed_data

def write_fixedCrds(fixedCoords: dict[str, list], y_center: float, z_center: float) -> str:
    """
    Write fixed coordinates into a PDB format-like string.

    This function first converts any partial coordinates to full 3D coordinates
    using the specified center values. Then, it formats the data into a string
    that resembles the PDB format, including a HEADER and ATOM records.

    Example PDB line format:
    ATOM      1 COM  A   _   1      -1.0000  25.000  25.000  1.00  0.00  

    Args:
        fixedCoords (dict[str,list]): A dictionary of coordinates.
        y_center (float): The default y-coordinate.
        z_center (float): The default z-coordinate.

    Returns:
        A string containing the coordinates in PDB format.
    """
    # First, get the full coordinates using the helper function
    full_coords_data = convert_to_full_coordinates(fixedCoords, y_center, z_center)
    
    # List to hold each line of the output file
    output_lines = []
    
    # Get the current date in YYYYMMDD format for the header
    import datetime
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    header = f"HEADER    FIXED MOLECULES                         {today_date}  NONE"
    output_lines.append(header)
    
    atom_index = 1
    # Iterate through each molecule and its coordinates
    for molecule_name, coordinates_list in full_coords_data.items():
        for atom_index_chain, coord in enumerate(coordinates_list):
            x, y, z = coord
            
            # Format the ATOM line according to the specified PDB-like format
            # f-string formatting is used to right-align numbers in their fields
            # add [:8] to enforce each coordinate only have 8 characters
            atom_line = (
                f"ATOM  {atom_index: >5}  COM{molecule_name:>4} _{atom_index_chain:>4}    "
                + f"{x: >8.3f}"[:8]
                + f"{y: >8.3f}"[:8]
                + f"{z: >8.3f}"[:8]
            )
            output_lines.append(atom_line)
            atom_index += 1
            
    # Join all lines with a newline character to form the final string
    return "\n".join(output_lines)

if __name__ == "__main__":
    InitialCoords = {}
    length = 120
    N_sites_half = 270
    xcrds = np.linspace(0.001, length-5.501, N_sites_half)
    InitialCoords['N'] = [[x-length/2] for x in xcrds]
    InitialCoords['S'] = [[-30]]
    InitialCoords['P'] = [[30, 5, 0]]
    y_center = 0
    z_center = 0
    print(write_fixedCrds(InitialCoords, y_center, z_center))