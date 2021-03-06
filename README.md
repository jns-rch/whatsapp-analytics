# whatsapp-analytics
 Analyze your whatsapp chats with python and plot fancy plots about you chat statistics. Access all the plots with [streamlit](https://www.streamlit.io/) in your browser.

## Setup

Install all the required packages with
````
pip install -r requirements.txt
````
## Extract WhatsApp chats
![alt text](/documentation/extract_chat.png "Extract WhatsApp text")

The text file has (beyond some special lines for media etc.) the following syntax:
```
DD.MM.YY, hh:mm - SENDER: MESSAGE
```
The file will first get cleaned and then stored in a Pandas dataframe.

## Usage
Use [streamlit](https://www.streamlit.io/) in your browser to access plots:
``` bash
streamlit run whatsapp-analytics-streamlit-plotly.py
```

Then you will need to type the folder containing your chat text files. That's because streamlit does not provide a proper functionality to import files from file explorer:

``` bash
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.108:8501

Folder: #INSERT_YOUR_FOLDER_HERE
```

## Examples
There are not all plots available in streamlit. If you want to see all plots refer to ```whatsapp-analytics.ipynb```.

Other examples can be seen here:

At first, select the chat file you want to analyze:
![Select_chat](documentation/Select_Chat.png "Select chat for analysis")

For some plots, a spcific user has to be chosen:
![Select_user](documentation/Select_User.png "Select user for analysis")

See a user specific plot:
![User_specific](documentation/User_specific.png "User specific plot")

## To-Do
- Include all plot from Jupyter Notebook in streamlit
- Make streamlit more interactive
- Analyze mood of the persons through messages
- ...
