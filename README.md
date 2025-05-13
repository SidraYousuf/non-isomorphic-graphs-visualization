
Built by https://www.blackbox.ai

---

# Non-Isomorphic Graphs with Degree Sequence Visualization

## Project Overview

This project provides an interactive visualization of two non-isomorphic graphs that share the same degree sequence of (3, 2, 2, 1). It uses HTML and JavaScript with the Cytoscape library to render the graphs, demonstrating how different graph structures can have identical degree sequences. The visual representation helps in understanding the concepts of graph isomorphism and degree sequences in graph theory.

## Installation

To run this project, simply download the `degree_sequence_graphs.html` file. There are no additional dependencies to install since the necessary libraries are loaded via CDN. Open the HTML file in any modern web browser.

1. Clone the repository or download the `degree_sequence_graphs.html` file.
```bash
git clone <repository_url>
```
2. Navigate to the downloaded folder.
```bash
cd <folder_name>
```
3. Open the file in your browser.
```bash
open degree_sequence_graphs.html # For macOS
# or
start degree_sequence_graphs.html # For Windows
```

## Usage

Once the HTML file is opened in a web browser, you will see two graphs displayed side by side. Each graph represents a different structure, while still having the same degree sequence. 

- **Graph 1** is a path-like structure with a central high-degree vertex.
- **Graph 2** is star-like with a prominent branch.

You can visually inspect the graphs and read the information provided about their structure and verification of their non-isomorphism.

## Features

- **Interactive Graph Visualization**: Utilizing Cytoscape.js for dynamic graph representation.
- **Responsiveness**: The layout adjusts according to the screen size.
- **Information on Isomorphism**: A detailed section explaining the verification of the non-isomorphism between the graphs.

## Dependencies

This project relies on the following libraries, which are included via CDN:

- [Tailwind CSS](https://tailwindcss.com/) for styling.
- [Cytoscape.js](https://js.cytoscape.org/) for graph rendering.

These libraries are linked in the HTML file as:
```html
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.26.0/cytoscape.min.js"></script>
```

## Project Structure

```
/degree_sequence_graphs.html    # The main HTML file containing the visualization
```

This structure consists primarily of the HTML file, where all the necessary scripts and styles are embedded.

## License

This project is open-source and available for anyone to use and modify. If you have any contributions or suggestions, feel free to reach out.