from .rate_limits import GEMINI_TPM, SAFE_TOKEN_MARGIN, MAX_BATCH_SIZE
from .token_utils import TokenEstimator


class BatchBuilder:

    def build(self, texts):

        max_tokens = int(GEMINI_TPM * SAFE_TOKEN_MARGIN)

        batches = []
        current_batch = []
        current_tokens = 0

        for text in texts:

            tokens = TokenEstimator.estimate(text)

            if (current_tokens + tokens > max_tokens or len(current_batch) >= MAX_BATCH_SIZE):

                batches.append(current_batch)

                current_batch = []
                current_tokens = 0

            current_batch.append(text)
            current_tokens += tokens

        if current_batch:
            batches.append(current_batch)

        return batches