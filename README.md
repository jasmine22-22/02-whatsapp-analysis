# WhatsApp Chat Analysis

A notebook for exploring message activity, media markers, and frequent words in a WhatsApp text export. The included sample is synthetic and does not represent real people or conversations.

## Tools

- Python
- pandas
- matplotlib
- seaborn
- wordcloud

## Run

From this folder, install the listed packages and open the notebook:

```powershell
python -m pip install -r requirements.txt
jupyter notebook whatsapp_analysis.ipynb
```

The notebook reads `data/sample_chat.txt` by default.

## Analyze Your Own Chat

Export a chat from WhatsApp and place the exported text file at `data/chat.txt`. Change the path in the first notebook cell from `data/sample_chat.txt` to `data/chat.txt`. Keep the anonymization cell in the notebook so real sender names are replaced before analysis.

The real chat is not included for privacy. `data/sample_chat.txt` is synthetic.
