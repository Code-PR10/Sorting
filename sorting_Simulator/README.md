# Sorting Algorithm Visualizer

An interactive Python application that visualizes and compares different sorting algorithms in real-time.

## Features

- **Visualization**: Watch sorting algorithms in action with step-by-step visualization
- **Comparison**: Compare different sorting algorithms' performance
- **Multiple Algorithms**: Includes Bubble Sort, Quick Sort, Merge Sort, Heap Sort, Insertion Sort, and Selection Sort
- **Customizable**: Adjust array size and sorting speed
- **Real-time Statistics**: Track comparisons, swaps, and execution time

## Requirements

- Python 3.7+
- customtkinter
- Pillow (PIL)
- numpy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/sorting_visualizer.git
cd sorting_visualizer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python sorting_visualizer.py
```

### Visualization Tab
- Select a sorting algorithm
- Adjust array size and sorting speed
- Click "Start Sorting" to begin visualization
- Use "Generate New Array" to create a new random array
- Enter custom array values if desired

### Comparison Tab
- Select two different algorithms to compare
- Enter test array sizes (comma-separated)
- Click "Start Comparison" to run the comparison
- View detailed performance metrics

## Project Structure

- `sorting_visualizer.py`: Main application file
- `sorting_algorithms.py`: Implementation of sorting algorithms
- `requirements.txt`: Project dependencies

## Contributing

Feel free to submit issues and enhancement requests! 