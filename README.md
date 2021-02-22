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
```
streamlit run whatsapp-analytics-streamlit-plotly.py
```

## Examples
There are not all plots available in streamlit. If you want to see all plots refer to ```whatsapp-analytics.ipynb```.

Other examples can be seen here:
![Select_chat](/documentation/Select_chat.png "Extract WhatsApp text")
![Select_user](/documentation/Select_user.png "Extract WhatsApp text")
![User_specific](/documentation/User_specific.png "Extract WhatsApp text")

## To-Do
- Include all plot from Jupyter Notebook in streamlit
- Make streamlit more interactive
- Analyze mood of the persons through messages
- ...
