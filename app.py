from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

candidates = []
companies = []

def calculate_match(candidate, company):
    score = 0
    
    skill_match = len([skill for skill in candidate["skills"] 
                      if skill in company["requirements"]])
    score += (skill_match / len(company["requirements"])) * 40 if company["requirements"] else 0
    
    accommodation_match = len([acc for acc in candidate["accommodations"] 
                             if acc in company["accommodations"]])
    score += (accommodation_match / len(candidate["accommodations"])) * 30 if candidate["accommodations"] else 0
    
    preference_match = len([pref for pref in candidate["workPreferences"] 
                          if pref in company["culture"]])
    score += (preference_match / len(candidate["workPreferences"])) * 30 if candidate["workPreferences"] else 0
    
    return round(score)

@app.route('/candidates', methods=['GET'])
def get_candidates():
    return jsonify(candidates)

@app.route('/candidates', methods=['POST'])
def add_candidate():
    candidate = request.json
    candidate['id'] = len(candidates) + 1
    candidates.append(candidate)
    return jsonify(candidate), 201

@app.route('/companies', methods=['GET'])
def get_companies():
    return jsonify(companies)

@app.route('/companies', methods=['POST'])
def add_company():
    company = request.json
    company['id'] = len(companies) + 1
    companies.append(company)
    return jsonify(company), 201

@app.route('/matches', methods=['GET'])
def get_matches():
    matches = []
    for candidate in candidates:
        for company in companies:
            match_score = calculate_match(candidate, company)
            matches.append({
                'candidate': candidate,
                'company': company,
                'score': match_score
            })
    
    matches.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True)