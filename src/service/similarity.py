from sentence_transformers import SentenceTransformer, SimilarityFunction
from torch import Tensor

# Load a pre-trained SBERT model
model = SentenceTransformer(
    "all-MiniLM-L6-v2", similarity_fn_name=SimilarityFunction.COSINE
)


def check_similarity(expected_answer: str, actual_answer: str) -> float:
    expected_embedding: Tensor = model.encode(expected_answer, convert_to_tensor=True)  # type: ignore
    actual_embedding: Tensor = model.encode(actual_answer, convert_to_tensor=True)  # type: ignore

    # Compute cosine similarity
    # similarity = util.cos_sim(expected_embedding, actual_embedding)
    similarity = model.similarity(expected_embedding, actual_embedding)  # type: ignore
    return similarity.item() * 100


# Example usage
if __name__ == "__main__":
    text1 = "Employees should book flight tickets befor 15 days of travel"
    text2 = "There is a total of 12 days of casual leave an employee can take in a year"
    similarity = check_similarity(text1, text2)
    print(f"Similarity percentage: {similarity:.2f}%")
