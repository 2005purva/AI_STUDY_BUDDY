import re
import random

class QuizGenerator:
    """Generates Multiple-Choice Questions (MCQs) and Spaced Repetition Flashcards from text chunks."""

    @staticmethod
    def generate_mcqs(chunks: list[dict], num_questions: int = 5) -> list[dict]:
        """Generates dynamic MCQs from key sentences across document chunks."""
        questions = []
        all_text = " ".join([c["text"] for c in chunks])
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', all_text) if len(s.strip()) > 35]

        if not sentences:
            return []

        candidate_sentences = [s for s in sentences if any(kw in s.lower() for kw in ['is', 'are', 'called', 'means', 'defined', 'used', 'can', 'provides', 'requires', 'contains'])]
        if len(candidate_sentences) < num_questions:
            candidate_sentences = sentences

        selected_sentences = random.sample(candidate_sentences, min(num_questions, len(candidate_sentences)))

        for idx, sentence in enumerate(selected_sentences):
            words = [w.strip('.,;()[]"') for w in sentence.split() if len(w.strip('.,;()[]"')) > 4 and w.lower() not in {'which', 'there', 'their', 'where', 'about', 'these', 'those', 'under', 'using'}]
            
            if not words:
                continue

            target_word = random.choice(words)
            question_text = sentence.replace(target_word, "__________")

            distractors = list(set([
                w.capitalize() for w in re.findall(r'\b[A-Za-z]{4,}\b', all_text) 
                if w.lower() != target_word.lower() and len(w) > 3
            ]))
            
            if len(distractors) < 3:
                distractors.extend(["Analysis", "Framework", "System", "Protocol", "Algorithm", "Variable"])

            random.shuffle(distractors)
            wrong_choices = distractors[:3]

            options = wrong_choices + [target_word]
            random.shuffle(options)

            questions.append({
                "id": idx + 1,
                "question": f"Q{idx + 1}: Complete the statement:\n\"{question_text}\"",
                "options": options,
                "answer": target_word,
                "explanation": f"The full original statement from the notes is: \"{sentence}\"."
            })

        return questions

    @staticmethod
    def generate_flashcards(chunks: list[dict], max_cards: int = 10) -> list[dict]:
        """Generates front/back study flashcards for active recall."""
        flashcards = []
        all_text = " ".join([c["text"] for c in chunks])
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', all_text) if len(s.strip()) > 40]

        for idx, sentence in enumerate(sentences[:max_cards]):
            words = sentence.split()
            if len(words) > 6:
                front_concept = " ".join(words[:5]) + "..."
                flashcards.append({
                    "id": idx + 1,
                    "front": f"What is discussed regarding: '{front_concept}'?",
                    "back": sentence,
                    "status": "New"
                })

        return flashcards
