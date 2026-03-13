class TokenEstimator:

    @staticmethod
    def estimate(text: str) -> int:
        return max(1, int(len(text) / 4))