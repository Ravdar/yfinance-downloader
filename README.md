
# <img src="https://user-images.githubusercontent.com/97836782/236618799-0301c964-239f-4e23-a6f7-0e2bcf7cfbb1.png" width="40" height="40"> YFinance downloader
This is a simple GUI application that allows users to download OHLC (Open, High, Low, Close) data from Yahoo Finance using the yfinance Python library. The application provides a quick and intuitive way to download the data and save it in a selected destination folder. It detects whether a date already exists in a given location and, if so, combines it, so you can collect data from a long periods of time.


<img src="https://user-images.githubusercontent.com/97836782/236618708-abc45d2d-bf94-48a6-8e3f-26b444f0f7db.png" width="538" height="566">

# Features
* User-friendly interface for downloading OHLC data from Yahoo Finance.
* Supports multiple tickers, periods, and intervals.
* Merging already existed data with new one
* Ability to select a destination folder for saving the downloaded data.
* Option to create an Excel file for the downloaded data.
* Load and save sets of tickers for easy reuse.

# Installation
1. Clone the repository:
```python
git clone https://github.com/Ravdar/YFinance-downloader
```
2. Install the required libraries:
```python
pip install -r requirements.txt
```

# Usage
1. Run the application.
2. Enter the ticker symbol(s) of the stocks you want to download OHLC data for.
3. Select the desired period and interval for the data.
4. Click the "+" button to add more tickers if needed.
5. Click the "-" button to remove the last added ticker.
6. Click the "Select destination" button to choose a folder for saving the downloaded data.
7. Check the "Create Excel file" checkbox if you want to generate an Excel file for the data.
8. Click the "Start" button to initiate the download process.
9. Wait for the download to complete. The status label will show the progress.
10. Once the download is finished, a message box will display the number of files downloaded and the data will be ready for use.

# Used libraires
* pandas
* yfinance
* customtkinter
* threading
* json

# Contributions
 
If you see some bugs or possible improvements, pelase contact me.
If you want to add a new feature or fix a bug by yourself, follow these steps:
1. Create a new branch for your changes.
2. Make your changes in the new branch.
3. Run tests and make sure that all tests pass.
4. Submit a pull request.

# Credits
Plus and minus icons used in the app are from [flaticon.com](https://www.flaticon.com/).
