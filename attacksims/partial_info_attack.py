import hashlib
import hmac
from typing import Tuple, Optional

class PartialInterceptAttack:
    """
    Partial-intercept attack implementation for cryptographic analysis.
    Simulates interception of partial data in a cryptographic protocol.
    """
    
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key
        self.intercepted_data = []
    
    def intercept_partial(self, data: bytes, intercept_ratio: float) -> Tuple[bytes, bytes]:
        """
        Intercept a partial fraction of transmitted data.
        
        Args:
            data: The data being transmitted
            intercept_ratio: Fraction of data to intercept (0.0 to 1.0)
            
        Returns:
            Tuple of (intercepted_portion, remaining_portion)
        """
        if not 0 <= intercept_ratio <= 1:
            raise ValueError("intercept_ratio must be between 0 and 1")
        
        split_point = int(len(data) * intercept_ratio)
        intercepted = data[:split_point]
        remaining = data[split_point:]
        
        self.intercepted_data.append(intercepted)
        return intercepted, remaining
    
    def analyze_intercepted(self) -> dict:
        """Analyze patterns in intercepted data."""
        if not self.intercepted_data:
            return {"status": "no_data_intercepted"}
        
        analysis = {
            "total_intercepts": len(self.intercepted_data),
            "total_bytes": sum(len(d) for d in self.intercepted_data),
            "average_size": sum(len(d) for d in self.intercepted_data) // len(self.intercepted_data),
            "signatures": []
        }
        
        for data in self.intercepted_data:
            sig = hashlib.sha256(data).hexdigest()
            analysis["signatures"].append(sig)
        
        return analysis
    
    def verify_integrity(self, data: bytes, signature: bytes) -> bool:
        """Verify if intercepted data matches HMAC signature."""
        expected_sig = hmac.new(self.secret_key, data, hashlib.sha256).digest()
        return hmac.compare_digest(signature, expected_sig)
    
    def reset(self):
        """Clear intercepted data."""
        self.intercepted_data = []


# Example usage
if __name__ == "__main__":
    secret = b"cryptographic_secret_key"
    attack = PartialInterceptAttack(secret)
    
    # Simulate data transmission
    transmitted_data = b"This is sensitive information that needs protection"
    
    # Intercept 40% of the data
    intercepted, remaining = attack.intercept_partial(transmitted_data, 0.4)
    
    print(f"Intercepted: {intercepted}")
    print(f"Remaining: {remaining}")
    print(f"Analysis: {attack.analyze_intercepted()}")
