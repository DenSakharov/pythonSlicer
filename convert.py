from stl import mesh

# Define the file paths
text_stl_file = "cube.stl"
binary_stl_file = "cube1.stl"

try:
    your_mesh = mesh.Mesh.from_file(text_stl_file)

    # Save it in binary format
    your_mesh.save(binary_stl_file)

    print(f"Successfully converted to binary STL: {binary_stl_file}")
except Exception as e:
    print(f"Error: {e}. The file is not in valid STL format.")
