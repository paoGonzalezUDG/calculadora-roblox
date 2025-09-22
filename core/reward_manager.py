import json
import os

class RewardManager:
    """Gestiona el desbloqueo de recompensas y el total de Robux."""
    def __init__(self, save_file='rewards.json'):
        self.save_file = save_file
        self.data = self._load_data()

    def _load_data(self):
        """Carga los datos desde un archivo JSON. Si no existe o está corrupto, crea un estado por defecto."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Asegurarse de que las claves existan para evitar errores
                    if "rewards" not in loaded_data:
                        loaded_data["rewards"] = {"oof_sound": False}
                    if "total_robux" not in loaded_data:
                        loaded_data["total_robux"] = 0
                    return loaded_data
            except (json.JSONDecodeError, IOError):
                return {"rewards": {"oof_sound": False}, "total_robux": 0}
        else:
            # Estado inicial de los datos
            return {"rewards": {"oof_sound": False}, "total_robux": 0}

    def _save_data(self):
        """Guarda el estado actual de los datos en el archivo JSON."""
        with open(self.save_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def unlock_reward(self, reward_id):
        """Desbloquea una recompensa y guarda el cambio."""
        if reward_id in self.data["rewards"] and not self.data["rewards"][reward_id]:
            print(f"¡Recompensa desbloqueada: {reward_id}!")
            self.data["rewards"][reward_id] = True
            self._save_data()
            return True
        return False

    def is_unlocked(self, reward_id):
        """Comprueba si una recompensa está desbloqueada."""
        return self.data["rewards"].get(reward_id, False)
    
    # --- FUNCIONES PARA ROBUX ---
    def add_robux(self, amount):
        """Añade o resta una cantidad de Robux al total y guarda."""
        current_robux = self.data.get("total_robux", 0)
        new_total = current_robux + amount
        
        # Evitar que los Robux sean negativos
        self.data["total_robux"] = max(0, new_total)
        
        self._save_data()
        print(f"Se modificaron {amount} Robux. Total: {self.data['total_robux']}")

    def get_total_robux(self):
        """Devuelve el total de Robux acumulados."""
        return self.data.get("total_robux", 0)

