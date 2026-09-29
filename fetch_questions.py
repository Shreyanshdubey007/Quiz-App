import json
import urllib.request
import html
import random
import time

categories_map = {
    "Science": [17, 18],     # 17: Science & Nature, 18: Computers
    "History": [23],         # 23: History
    "Sports": [21],          # 21: Sports
    "General Knowledge": [9] # 9: General Knowledge
}

difficulties = ["easy", "hard"]
questions_list = []

print("Fetching new questions from OpenTDB API...")

for cat_name, cat_ids in categories_map.items():
    for diff in difficulties:
        for cat_id in cat_ids:
            amount = 25 if len(cat_ids) == 2 else 50
            url = f"https://opentdb.com/api.php?amount={amount}&category={cat_id}&difficulty={diff}&type=multiple"
            try:
                print(f"Fetching {amount} {diff} questions for {cat_name} (ID: {cat_id})...")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                    
                    if data['response_code'] == 0:
                        for item in data['results']:
                            question = html.unescape(item['question'])
                            correct = html.unescape(item['correct_answer'])
                            incorrects = [html.unescape(x) for x in item['incorrect_answers']]
                            
                            options = incorrects + [correct]
                            random.shuffle(options)
                            
                            correct_idx = options.index(correct)
                            correct_letter = "ABCD"[correct_idx]
                            
                            diff_capitalized = diff.capitalize()
                            
                            questions_list.append((
                                question, options[0], options[1], options[2], options[3],
                                correct_letter, cat_name, diff_capitalized
                            ))
                    else:
                        print(f"Failed to fetch data, response code: {data['response_code']}")
                
                # API rate limit spacing
                time.sleep(5)
            except Exception as e:
                print(f"Error fetching {cat_name} {diff}: {e}")

# Combine with existing 40 questions to preserve the originals
try:
    from database.questions_data import QUESTIONS as original_q
    final_questions = original_q + questions_list
except Exception as e:
    print("Could not import existing questions:", e)
    final_questions = questions_list

print(f"\nWriting {len(final_questions)} total questions to questions_data.py...")

with open('database/questions_data.py', 'w', encoding='utf-8') as f:
    f.write('"""\nquestions_data.py  –  Pre-loaded question bank.\n\n')
    f.write('Each tuple follows the schema:\n')
    f.write('    (question, option_a, option_b, option_c, option_d,\n')
    f.write('     correct_option, category, difficulty)\n')
    f.write('"""\n\n')
    
    f.write('QUESTIONS = [\n')
    for q in final_questions:
        q_escaped = [str(x).replace('"', '\\"').replace('\n', ' ') for x in q]
        f.write(f'    ("{q_escaped[0]}", "{q_escaped[1]}", "{q_escaped[2]}", "{q_escaped[3]}", "{q_escaped[4]}", "{q_escaped[5]}", "{q[6]}", "{q[7]}"),\n')
    f.write(']\n')

print("Done! 🎉 Database will refresh on next app launch.")
