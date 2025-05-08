# Dream Journal

Dream Journal is a desktop application developed in Python that allows users to record, analyze, and visualize their dreams. This project is designed for anyone who wants to keep track of their dreams, analyze them over time, and discover patterns or interesting details.

## Features

- **Dream Logging**: Record details such as the date, title, description, tags, vividness, whether the dream was lucid, sleep satisfaction, hours slept, and the technique used.
- **Advanced Filters**: Filter dreams by tags, sort by date, vividness, or satisfaction.
- **Interactive Graphs**: View graphs to analyze vividness, lucid dreams, sleep satisfaction, and hours slept within a specific date range.
- **Data Export**: Data is saved in a CSV file for easy access and external analysis.

## How to Use

1. **Installation**:
   - Ensure you have Python 3.10 or higher installed on your system.
   - Install the required dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

2. **Launching the Application**:
   - Run the `main.py` file:
     ```bash
     python main.py
     ```

3. **Logging a Dream**:
   - Fill in the required fields in the form and click "💾 Save" to log the dream.

4. **Viewing Dreams**:
   - Click "📖 Read Dreams" to view logged dreams.
   - Use filters to search for specific dreams or sort them.

5. **Data Analysis**:
   - Click "📊 Graphs" to view interactive graphs based on dream data.
   - Select the date range and desired graph type.

## When to Use

- To keep track of your dreams and analyze them over time.
- For those interested in studying lucid dreams or improving sleep quality.
- To explore patterns in your dreams and discover correlations between sleep techniques and dream quality.

## Requirements

- Python 3.10 or higher
- Python Libraries:
  - `tkinter`
  - `pandas`
  - `matplotlib`
  - `tkcalendar`

## Contributions

Contributions, suggestions, and bug reports are welcome! Feel free to open an issue or submit a pull request.

## License

This project is distributed under the MIT License. See the LICENSE file for more details.