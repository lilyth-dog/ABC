import numpy as np
import time
import logging

# Mock gRPC stubs for standalone testing
# from proto import neuro_signal_pb2, neuro_signal_pb2_grpc

class ReservoirReadout:
    """
    Implements the spatial readout layer defined in Research Paper Section 4.4.
    Maps high-dimensional magnetic states (Reservoir) to low-dimensional kinematics (Readout).
    """
    def __init__(self, input_dim=128*128, output_dim=20, ridge_alpha=1.0):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.ridge_alpha = ridge_alpha
        
        # Initialize weights (W_out) with small random values
        self.W_out = np.random.randn(output_dim, input_dim) * 0.01
        self.bias = np.zeros(output_dim)

    def predict(self, magnetic_state):
        """
        y(t) = W_out * m(t) + b
        """
        # Flatten state if necessary (e.g. 128x128 grid -> 16384 vector)
        m_vec = magnetic_state.flatten()
        return np.dot(self.W_out, m_vec) + self.bias

    def update_hebbian(self, magnetic_state, current_output, target_output, learning_rate=0.001):
        """
        Hebbian Learning Rule (Eq. in Section 4.4):
        dW_ij = eta * (Target_j - y_j) * m_i
        """
        m_vec = magnetic_state.flatten()
        error = target_output - current_output
        
        # Outer product to calculate dW for all i, j
        delta_W = learning_rate * np.outer(error, m_vec)
        
        self.W_out += delta_W
        self.bias += learning_rate * error # Simple bias update

class BehavioralPersonalityDecoder:
    """
    Decodes user interaction patterns into high-level personality traits (Neuro-Traits).
    Maps behavioral metrics to 'Synthetic EEG' values.
    
    Now supports cultural context for bias mitigation (Phase 2 improvement).
    """
    def __init__(self, cultural_context: str = "default"):
        self.cultural_context = cultural_context
        self.cultural_weights = self._load_cultural_weights()
    
    def _load_cultural_weights(self) -> dict:
        """Load cultural weight modifiers from JSON configuration."""
        import json
        import os
        
        config_path = os.path.join(os.path.dirname(__file__), "cultural_weights.json")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("cultures", {})
        except FileNotFoundError:
            print("[BehavioralPersonalityDecoder] cultural_weights.json not found, using defaults")
            return {}
        except Exception as e:
            print(f"[BehavioralPersonalityDecoder] Error loading cultural weights: {e}")
            return {}
    
    def set_cultural_context(self, context: str):
        """Update cultural context for personalization."""
        if context in self.cultural_weights or context == "default":
            self.cultural_context = context
            return True
        return False
    
    def get_available_cultures(self) -> list:
        """Return list of supported cultural contexts."""
        return list(self.cultural_weights.keys())
    
    def _apply_cultural_modifiers(self, weights: dict) -> dict:
        """Apply cultural weight modifiers to baseline personality weights."""
        culture_config = self.cultural_weights.get(self.cultural_context, {})
        modifiers = culture_config.get("modifiers", {})
        
        # Apply latency interpretation modifier
        latency_mod = modifiers.get("latency_interpretation", {})
        logic_boost = latency_mod.get("logic_weight_boost", 0.0)
        intuition_reduction = latency_mod.get("intuition_weight_reduction", 0.0)
        
        # Apply revision interpretation modifier
        revision_mod = modifiers.get("revision_interpretation", {})
        complexity_boost = revision_mod.get("complexity_weight_boost", 0.0)
        
        # Apply efficiency interpretation modifier
        efficiency_mod = modifiers.get("efficiency_interpretation", {})
        fluidity_boost = efficiency_mod.get("fluidity_weight_boost", 0.0)
        
        # Create adjusted weights
        adjusted = {
            "Logic": min(weights["Logic"] + logic_boost, 1.0),
            "Intuition": max(weights["Intuition"] - intuition_reduction, 0.0),
            "Fluidity": min(weights["Fluidity"] + fluidity_boost, 1.0),
            "Complexity": min(weights["Complexity"] + complexity_boost, 1.0)
        }
        
        return adjusted
    
    def _get_cultural_archetype(self, weights: dict) -> str:
        """Generate culturally-appropriate archetype name."""
        culture_config = self.cultural_weights.get(self.cultural_context, {})
        archetype_mappings = culture_config.get("archetype_mappings", {})
        
        logic = weights.get("Logic", 0.5)
        intuition = weights.get("Intuition", 0.5)
        fluidity = weights.get("Fluidity", 0.5)
        complexity = weights.get("Complexity", 0.5)
        
        # Determine archetype key
        if logic > 0.6 and complexity > 0.6:
            key = "high_logic_high_complexity"
        elif intuition > 0.6 and fluidity > 0.6:
            key = "high_intuition_high_fluidity"
        else:
            key = "balanced"
        
        return archetype_mappings.get(key, "Balanced & Steady")
    
    def decode(self, profile):
        # profile: {pathEfficiency, avgDecisionLatency, revisionRate, jitterIndex, intensity, contextualChoices}
        
        choices = profile.get('contextualChoices', {})
        aesthetics = choices.get('aesthetics', 'Cyber/Industrial')
        trait_weights = choices.get('traitWeights', {})
        
        # Get cultural context from profile if provided
        cultural_context = profile.get('culturalContext', self.cultural_context)
        if cultural_context != self.cultural_context:
            self.set_cultural_context(cultural_context)
        
        latency = profile.get('avgDecisionLatency', 1000)
        revisions = profile.get('revisionRate', 0)
        efficiency = profile.get('pathEfficiency', 1.0)
        maturity_level = profile.get('maturityLevel', 1)
        
        # --- Hierarchical Thresholds (DTMM) ---
        # Level 1 (Echo): Collapse weak signals to neutral (0.5)
        # Level 2 (Reflection): Moderate signal sensitivity
        # Level 3 (Synthesis): Full sensitivity
        signal_sensitivity = 0.3 if maturity_level == 1 else 0.7 if maturity_level == 2 else 1.0
        
        # --- Self-Exploration Weighting Logic ---
        
        # 1. Logic vs Intuition Weighting
        # Base weights on latency: Slow latency (>3s) -> Logic; Fast latency (<1.5s) -> Intuition
        logic_weight = min(max((latency - 1000) / 4000, 0.0), 1.0)
        intuition_weight = 1.0 - logic_weight
        
        # 2. Fluidity Weight (Confidence/Stability)
        fluidity_weight = efficiency
        
        # 3. Complexity (Engagement/Detail focus)
        # More revisions + high latency -> High complexity
        complexity_weight = min((revisions * 0.2) + (latency / 10000), 1.0)

        # Base weights before cultural adjustment
        base_weights = {
            "Logic": round(logic_weight, 2),
            "Intuition": round(intuition_weight, 2),
            "Fluidity": round(fluidity_weight, 2),
            "Complexity": round(complexity_weight, 2)
        }
        
        # Apply cultural modifiers
        adjusted_weights = self._apply_cultural_modifiers(base_weights)
        
        # Update local variables for downstream logic
        logic_weight = adjusted_weights["Logic"]
        intuition_weight = adjusted_weights["Intuition"]
        fluidity_weight = adjusted_weights["Fluidity"]
        complexity_weight = adjusted_weights["Complexity"]

        # Determine Primary Trait
        is_analytical = logic_weight > 0.6 or revisions > 3
        
        # 4. Aesthetics influence (Vibe)
        if aesthetics == 'Zen/Minimal':
            theta = 0.9
            beta = 0.1
        elif aesthetics == 'Neon/Vibrant':
            theta = 0.1
            beta = 0.9
        else: # Cyber/Industrial
            theta = 0.4
            beta = 0.6
            
        if is_analytical:
            theta = min(theta + 0.2, 0.95)
            beta = max(beta - 0.2, 0.05)
            
        # 5. Experience/Achievement
        task_completion = profile.get('taskCompletion', 0)
        txp = (efficiency * 0.3) + (task_completion * 0.7)
        
        # Get cultural archetype
        cultural_archetype = self._get_cultural_archetype(adjusted_weights)
        
        # 6. DTMM Confidence Calibration
        # Apply signal sensitivity to weights: closer to 0.5 if low maturity
        def calibrate(w, sensitivity):
            return 0.5 + (w - 0.5) * sensitivity

        calibrated_weights = {
            k: round(calibrate(v, signal_sensitivity), 2) 
            for k, v in adjusted_weights.items()
        }
        
        # Sync Score calculation (how closely the twin matches the persona)
        sync_score = min(txp * 0.5 + (1.0 - abs(0.5 - calibrated_weights["Logic"])) * 0.5, 1.0)

        return {
            "synthetic_theta": theta,
            "synthetic_beta": beta,
            "aesthetics": aesthetics,
            "twin_experience": txp,
            "cultural_context": self.cultural_context,
            "maturity_level": maturity_level,
            "sync_score": round(sync_score, 2),
            "traits": {
                "analytical": is_analytical,
                "stable": efficiency > 0.5,
                "weights": calibrated_weights,
                "base_weights": base_weights,
                "cultural_adjustment_applied": self.cultural_context != "default",
                "cultural_archetype": cultural_archetype,
                "evidence": {
                    "reasoning": "High revision rate" if revisions > 2 else "Rapid decision flow" if latency < 1500 else "Balanced deliberation",
                    "latency_ms": latency,
                    "revisions": revisions,
                    "cultural_context": self.cultural_context,
                    "maturity_level": maturity_level
                },
                "experience_level": "Novice" if txp < 0.5 else "Adept" if txp < 0.8 else "Master"
            }
        }

class ContinuousLearner:
    """
    Continuous Learning Engine for Digital Human Twin.
    Implements incremental personality weight updates using exponential moving average.
    Enables hyper-personalization over multiple sessions.
    """
    def __init__(self, learning_rate: float = 0.3):
        self.learning_rate = learning_rate  # EMA alpha (higher = faster adaptation)
    
    def update_weights(self, current_weights: dict, new_weights: dict) -> dict:
        """
        Exponential Moving Average (EMA) update:
        W_new = alpha * W_session + (1 - alpha) * W_history
        
        This allows recent sessions to influence the profile while
        maintaining stability from historical data.
        """
        updated = {}
        alpha = self.learning_rate
        
        for key in new_weights:
            if key in current_weights:
                # EMA update
                updated[key] = round(
                    alpha * new_weights[key] + (1 - alpha) * current_weights[key], 
                    2
                )
            else:
                updated[key] = new_weights[key]
        
        return updated
    
    def calculate_drift(self, history: list) -> dict:
        """
        Detect significant changes in personality weights over time.
        Returns drift analysis for each trait.
        """
        if len(history) < 2:
            return {"status": "insufficient_data", "sessions_needed": 2 - len(history)}
        
        # Compare first and last profiles
        first = history[0]
        last = history[-1]
        
        traits = ["logic_weight", "intuition_weight", "fluidity_weight", "complexity_weight"]
        drift_report = {}
        
        for trait in traits:
            if trait in first and trait in last:
                delta = last[trait] - first[trait]
                drift_report[trait] = {
                    "initial": first[trait],
                    "current": last[trait],
                    "delta": round(delta, 3),
                    "direction": "increasing" if delta > 0.05 else "decreasing" if delta < -0.05 else "stable",
                    "magnitude": "significant" if abs(delta) > 0.15 else "moderate" if abs(delta) > 0.08 else "minor"
                }
        
        return {
            "status": "analyzed",
            "session_count": len(history),
            "traits": drift_report
        }
    
    def compute_confidence(self, session_count: int, weight_stability: float) -> float:
        """
        Confidence score based on:
        1. Number of sessions (more data = higher confidence)
        2. Weight stability (consistent weights = higher confidence)
        """
        # Session factor: saturates around 10 sessions
        session_factor = min(session_count / 10, 1.0)
        
        # Stability factor (1.0 = perfectly stable)
        stability_factor = weight_stability
        
        # Combined score
        confidence = 0.4 * session_factor + 0.6 * stability_factor
        return round(confidence, 2)
    
    def generate_archetype(self, weights: dict) -> str:
        """
        Generate personality archetype based on dominant traits.
        """
        logic = weights.get("Logic", 0.5)
        intuition = weights.get("Intuition", 0.5)
        fluidity = weights.get("Fluidity", 0.5)
        complexity = weights.get("Complexity", 0.5)
        
        # Primary dimension
        if logic > intuition + 0.2:
            primary = "Analytical"
        elif intuition > logic + 0.2:
            primary = "Intuitive"
        else:
            primary = "Balanced"
        
        # Secondary dimension
        if fluidity > 0.6:
            secondary = "& Adaptive"
        elif complexity > 0.6:
            secondary = "& Complex"
        else:
            secondary = "& Steady"
        
        return f"{primary} {secondary}"


class MagnonicController:
    """
    Orchestrates the data flow: EEG -> Physics Params -> Simulation -> Readout -> Kinematics.
    Now uses pre-computed MuMax3 database for physics-accurate results.
    """
    def __init__(self):
        self.readout = ReservoirReadout()
        self.behavior_decoder = BehavioralPersonalityDecoder()
        self.running = False
        self._init_simulation_db()
        print("[MagnonicController] Initialized with 128x128 reservoir grid and Behavior Decoder.")

    def _init_simulation_db(self):
        """Initialize pre-computed MuMax3 database"""
        try:
            from simulation_db import get_simulation_db
            self.sim_db = get_simulation_db()
            self.use_precomputed = True
            print("[MagnonicController] Using pre-computed MuMax3 patterns")
        except ImportError:
            self.sim_db = None
            self.use_precomputed = False
            print("[MagnonicController] Fallback to mock simulation")
        
        # MuMax3 실시간 통합 초기화 (선택적)
        try:
            from mumax3_integration import get_mumax3_integration
            self.mumax3 = get_mumax3_integration()
            if self.mumax3.available and self.mumax3.enable_realtime:
                print("[MagnonicController] MuMax3 real-time simulation enabled")
        except ImportError:
            self.mumax3 = None

    def process_eeg_stream(self, theta_power, beta_power):
        """
        Processes EEG via the causal chain:
        1. Neuro-Magnetic Modulation (Theta -> Damping, Beta -> Excitation)
        2. Magnonic Reservoir Dynamics (Pre-computed MuMax3)
        3. Kinematic Readout
        """
        t = time.time()
        
        # 1. Get physics parameters
        alpha = 0.01 + 0.05 * theta_power
        b_ext_magnitude = 0.05 * beta_power
        
        # 2. Get magnetic state from pre-computed database or real-time simulation
        if hasattr(self, 'mumax3') and self.mumax3 and self.mumax3.enable_realtime:
            # 실시간 MuMax3 시뮬레이션 시도
            realtime_state = self.mumax3.run_simulation(theta_power, beta_power)
            if realtime_state is not None:
                magnetic_state = realtime_state
                physics_meta = self.mumax3.get_physics_metadata(theta_power, beta_power)
            elif self.use_precomputed and self.sim_db:
                # 실시간 실패 시 Pre-computed 사용
                magnetic_state = self.sim_db.get_magnetic_state(theta_power, beta_power, t)
                physics_meta = self.sim_db.get_physics_metadata(theta_power, beta_power)
            else:
                # Fallback: simple wave pattern
                grid_size = 128
                x = np.linspace(-5, 5, grid_size)
                y = np.linspace(-5, 5, grid_size)
                X, Y = np.meshgrid(x, y)
                R = np.sqrt(X**2 + Y**2)
                magnetic_state = np.sin(R - 2*np.pi*2.0*t) * np.exp(-0.1 * R * alpha) * b_ext_magnitude
                physics_meta = {"source": "mock"}
        elif self.use_precomputed and self.sim_db:
            magnetic_state = self.sim_db.get_magnetic_state(theta_power, beta_power, t)
            physics_meta = self.sim_db.get_physics_metadata(theta_power, beta_power)
        else:
            # Fallback: simple wave pattern
            grid_size = 128
            x = np.linspace(-5, 5, grid_size)
            y = np.linspace(-5, 5, grid_size)
            X, Y = np.meshgrid(x, y)
            R = np.sqrt(X**2 + Y**2)
            magnetic_state = np.sin(R - 2*np.pi*2.0*t) * np.exp(-0.1 * R * alpha) * b_ext_magnitude
            physics_meta = {"source": "mock"}
        
        # 3. Readout (Section 4.4)
        kinematics = self.readout.predict(magnetic_state)
        
        # Calculate Fluidity (Jerk proxy: inverse of high-freq noise)
        fluidity = 1.0 / (1.0 + np.var(kinematics))
        
        return {
            "joint_angles": kinematics.tolist(),
            "fluidity_index": fluidity,
            "sim_params": {
                "alpha": alpha, 
                "b_ext": b_ext_magnitude, 
                "theta": theta_power, 
                "beta": beta_power
            },
            "physics": physics_meta
        }

    def simulate_action_pattern(self, action_name):
        """
        Simulates EEG patterns corresponding to specific physical actions.
        Maps Action -> (Theta, Beta) -> Physics Parameters.
        
        [Data Source Methodology]
        Currently using: "Synthetic Heuristic Data" based on Neuro-Physiological Arousal Theory.
        - STAND: Low Arousal (Relaxation) -> High Theta / Low Beta.
        - RUN: High Arousal (Active Motor Drive) -> Low Theta / High Beta.
        
        [Real-World Collection Protocol]
        To replace this with real data:
        1. Hardware: OpenBCI / NueroSky EEG Headset.
        2. Task: Motor Imagery (MI) - Subject imagines 'Walking' or 'Running'.
        3. Processing: Real-time FFT to extract Power Spectral Density (PSD) in 4-8Hz and 13-30Hz bands.
        """
        if action_name == "STAND":
            # Stability focus: High Theta, Low Beta
            return self.process_eeg_stream(theta_power=0.8, beta_power=0.1)
        elif action_name == "WALK":
            # Rhythmic balance: Moderate Theta, Moderate Beta
            return self.process_eeg_stream(theta_power=0.4, beta_power=0.5)
        elif action_name == "RUN":
            # High drive/responsiveness: Low Theta, High Beta
            return self.process_eeg_stream(theta_power=0.1, beta_power=0.9)
        else:
            return self.process_eeg_stream(0.5, 0.5)

    def process_behavioral_profile(self, profile):
        """
        Entry point for Phase 6 Behavioral Analysis.
        Converts browser metrics into а바타 (Avatar) kinematics.
        """
        decoded = self.behavior_decoder.decode(profile)
        result = self.process_eeg_stream(
            theta_power=decoded["synthetic_theta"],
            beta_power=decoded["synthetic_beta"]
        )
        result["behavioral_traits"] = decoded["traits"]
        result["aesthetics"] = decoded["aesthetics"]
        
        # Aesthetic to visual world mapping
        vis_map = {
            'Zen/Minimal': {'fog_color': '#e0f7fa', 'glow': 0.3},
            'Cyber/Industrial': {'fog_color': '#001a1a', 'glow': 0.8},
            'Neon/Vibrant': {'fog_color': '#1a001a', 'glow': 1.5}
        }
        result["world_params"] = vis_map.get(decoded["aesthetics"])
        
        return result


if __name__ == "__main__":
    controller = MagnonicController()
    
    # Simulation Scenario: Relax -> Focus Transition
    print("\n[Scenario] User State: Deep Relaxation (Theta High)")
    for i in range(3):
        # Relax: High Theta (0.9), Low Beta (0.2)
        res = controller.process_eeg_stream(theta_power=0.9, beta_power=0.2)
        print(f"Time {i*0.1:.1f}s | Theta: 0.9 | Alpha: {res['sim_params']['alpha']:.4f} (High Damping) -> Fluidity: {res['fluidity_index']:.4f}")
        time.sleep(0.1)

    print("\n[Scenario] User State: Intense Focus (Beta High)")
    for i in range(3):
        # Focus: Low Theta (0.1), High Beta (0.95)
        res = controller.process_eeg_stream(theta_power=0.1, beta_power=0.95)
        print(f"Time {0.3+i*0.1:.1f}s | Beta: 0.95 | Alpha: {res['sim_params']['alpha']:.4f} (Low Damping)  -> Fluidity: {res['fluidity_index']:.4f}")
        time.sleep(0.1)
