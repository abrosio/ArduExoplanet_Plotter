# ArduExoplanet_Plotter

ArduExoplanet Plotter is a program designed to monitor and visualize in real-time data from a photoresistor connected to a microcontroller such as Arduino. The goal is to simulate photometry experiments used in the observation of exoplanets.

## Key Features

- **Real-time plotting** of photoresistor data.
- **Data logging** to a file.
- **Dynamic adjustment** of plot update speed.
- **Graph screenshot** directly from the interface.
- Compatibility with various serial ports and baud rates.

## Requirements

- Python 3.7 or later
- Arduino or another microcontroller configured to send photoresistor data via a serial port

## Installation

1. **Clone the Repository**

   ```bash
git clone https://github.com/your-username/ArduExoplanet.git
cd ArduExoplanet
   ```

2. **Set Up the Environment**

   Ensure the dependencies are installed. If not, use the command above.

3. **Prepare Arduino**

   Upload a sketch to Arduino that sends photoresistor data via the serial port.

4. **Run the Program**

   Launch the program with:

   ```bash
   python main.py
   ```

## Usage

1. Connect your Arduino (or another microcontroller) to your PC.
2. Select the correct serial port and baud rate from the interface.
3. Press "Start" to begin receiving and plotting data.
4. Use the buttons to:
   - **Save data** to a log file
   - **Reset the graph**
   - **Save a screenshot** of the graph
   - **Update the plot speed**

## Interface Preview

Here is a preview of the user interface:

![Interface Example](screenshot.png)

## Contributing

Contributions to the project are welcome! Feel free to open an issue or a pull request to suggest improvements or report problems.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

© 2024 Antonino Brosio - [www.antoninobrosio.it](https://www.antoninobrosio.it)

Thank you for using ArduExoplanet! If you have any questions or suggestions, don't hesitate to get in touch.
