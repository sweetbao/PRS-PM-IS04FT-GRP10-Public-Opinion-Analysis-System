```
pip install -r requirements.txt
```

Download pretrained bert model file to `./bert-base-uncased`
https://drive.google.com/drive/folders/18UwFy_7vD2ssGo76FRMO0r0tYSjfHmFs?usp=sharing

Download our model file to `./checkpoints`
https://drive.google.com/drive/folders/1td7h1gs2Uu6ia9MO6jvBOL-HRht-0EnK?usp=sharing

(Optional) Download dataset to `./twitter_data`
https://drive.google.com/drive/folders/1rQ980YQtx0giIIj-NXFTz93G3pLbchtV?usp=sharing

Do prediction:
```
python infer.py --model your_pth_model_path --model_type {bert, bert_cnn}
```

Call predict method:
```
from infer import get_prediction
get_prediction(raw_text_list)
```
