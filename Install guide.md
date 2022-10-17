# Public Opinion Analysis system installation guide


1. Need to install python(3.8) and node.js(18.10.0) properly in the environment
2. git clone git@github.com:sweetbao/PRS-Public-Opinion-Anakysis.git
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. cd backend
7. Download pretrained bert model file to `./SentimentModel/bert-base-uncased` (please create this folder if not exist)
    https://drive.google.com/drive/folders/18UwFy_7vD2ssGo76FRMO0r0tYSjfHmFs?usp=sharing

8. Download our model file to `./SentimentModel/checkpoints`(please create this folder if not exist)
    https://drive.google.com/drive/folders/1td7h1gs2Uu6ia9MO6jvBOL-HRht-0EnK?usp=sharing

9. python manage.py makemigrations
10. python manage.py migrate
11. python manage.py runserver
12. Open an other terminate
13. cd frontend
14. npm install
15. npm fund
16. npm audit fix
17. npm run dev
18. go to relate url see the result




