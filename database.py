import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cert_url = "" # ! ! !
cred = credentials.Certificate(requests.get(cert_url).json())
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_scores():
    docs = db.collection('scoresCollection').stream()

    all_docs_data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        all_docs_data.append(doc_data)

    return all_docs_data


def send_score(nickname, kills, wave, minutes, seconds):
    top_scores = get_scores()
    all_scores = []
    for score in top_scores:
        all_scores.append((score.get('nickname'),
                           score.get('kills'),
                           score.get('wave'),
                           score.get('minutes'),
                           score.get('seconds')))
    all_scores.append((nickname, kills, wave, minutes, seconds))

    sorted_scores = sorted(all_scores, key=lambda x: (-x[1], x[3]*60 + x[4]))

    for i in range(len(sorted_scores) - 1):
        db.collection('scoresCollection').document(str(i)).set({
            'nickname': sorted_scores[i][0],
            'kills': sorted_scores[i][1],
            'wave': sorted_scores[i][2],
            'minutes': sorted_scores[i][3],
            'seconds': sorted_scores[i][4]
        })


def reformat_data(db_scores):
    scores = []
    for score in db_scores:
        new_score = [(a, b) for a, b in score.items()]
        scores.append((new_score[4][1], new_score[0][1], new_score[3][1], new_score[2][1], new_score[1][1]))
    return scores
