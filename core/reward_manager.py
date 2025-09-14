import json
import os

class RewardManager:
    """Gestiona el desbloqueo y guardado de recompensas."""
    def __init__(self, save_file='rewards.json'):
        self.save_file = save_file
        self.rewards = self._load_rewards()

    def _load_rewards(self):
        """Carga las recompensas desde un archivo JSON. Si no existe, crea un estado por defecto."""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        else:
            # Estado inicial de las recompensas (todas bloqueadas)
            return {"oof_sound": False}

    def _save_rewards(self):
        """Guarda el estado actual de las recompensas en el archivo JSON."""
        with open(self.save_file, 'w') as f:
            json.dump(self.rewards, f)

    def unlock_reward(self, reward_id):
        """Desbloquea una recompensa y guarda el cambio."""
        if reward_id in self.rewards and not self.rewards[reward_id]:
            print(f"¡Recompensa desbloqueada: {reward_id}!")
            self.rewards[reward_id] = True
            self._save_rewards()
            return True # Indica que se acaba de desbloquear
        return False

    def is_unlocked(self, reward_id):
        """Comprueba si una recompensa está desbloqueada."""
        return self.rewards.get(reward_id, False)