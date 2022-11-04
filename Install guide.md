# Public Opinion Analysis system installation guide

### [ 1 ] System Environment Requirement

1. Install [nodejs (npm)>=18.10.0](https://nodejs.org/en/download/) on the computer

2. Install [python >=3.8](https://www.python.org/downloads/)

3. Google Chrome (latest version)

4. Install latest git version


### [ 2 ] Prepare basic project enviorment and create an virtual enviorment of python

1. Create a folder in computer to storage the project file and open a terminal in this folder:
 >git clone https://github.com/sweetbao/PRS-Public-Opinion-Anakysis.git
 >cd PRS-Public-Opinion-Anakysi
 >python -m venv venv
 >venv\Scripts\activate(windows) OR: source venv/bin/activate(mac)
 >pip install -r requirements.txt
 
2. Download pretrained bert model file(pytorch_model.bin) to `./TextEmotion/SentimentModel/bert-base-uncased`
    https://drive.google.com/drive/folders/18UwFy_7vD2ssGo76FRMO0r0tYSjfHmFs?usp=sharing

3. Download our model files to `./TextEmotion/SentimentModel/checkpoints`(please create this folder if not exist)
    https://drive.google.com/drive/folders/1td7h1gs2Uu6ia9MO6jvBOL-HRht-0EnK?usp=sharing


### [ 3 ] Deploy the Paper Recommendation system locally with virtual enviorment just created

1. In project folder terminal(with vertual environment activated) : 
 >cd backend
 >python manage.py runserver (ignore the migrate error)
 
2. Open an other terminal in project folder:
 >cd frontend
 >npm install (optional:npm audit fix)
 >npm fund 
 >npm run dev


### [ 4 ] Run the systems on browser
Go to URL using web browser** http://localhost:5173 or http://127.0.0.1:5173
Or: Directly click the link displayed on the frontend terminal

