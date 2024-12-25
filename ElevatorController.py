class Elevator:
    def __init__(self, initial_floor, max_floor, min_floor=1):
        self.current_floor = initial_floor
        self.max_floor = max_floor
        self.min_floor = min_floor
        self.steps = 0
        self.state = "IDLE"
        self.door_open = False
        self.direction = None
        self.command_log = []
        self.task_queue = []

    def move_up(self):
        self.current_floor += 1
        self.steps += 1
        self.direction = "up"
        self.state = "MOVING"
        self.command_log.append(f"Проехать этаж вверх -> {self.current_floor}")

    def move_down(self):
        self.current_floor -= 1
        self.steps += 1
        self.direction = "down"
        self.state = "MOVING"
        self.command_log.append(f"Проехать этаж вниз -> {self.current_floor}")

    def open_door(self):
        self.door_open = True
        self.state = "DOORS_OPEN"
        self.direction = None
        self.command_log.append("Открыть двери")

    def close_door(self):
        self.door_open = False
        self.state = "IDLE"
        self.command_log.append("Закрыть двери")

    def add_task(self, floor):
        self.task_queue = sorted(set(self.task_queue + [floor]), reverse=(self.direction == "down"))

    def reset_steps(self):
        self.steps = 0

    def get_commands(self):
        return self.command_log


class ElevatorController:
    def __init__(self, num_floors, elevators_positions):
        self.num_floors = num_floors
        self.elevators = [Elevator(pos, num_floors) for pos in elevators_positions]
        self.calls = {floor: {"up": False, "down": False} for floor in range(1, num_floors + 1)}
        self.calls[1]["down"] = None
        self.calls[num_floors]["up"] = None

    def find_best_elevator(self, call_floor, direction):
        is_suitable = lambda elevator: (
            elevator.state == "IDLE" or
            (elevator.direction == direction and
             (direction == "up" and elevator.current_floor <= call_floor) or
             (direction == "down" and elevator.current_floor >= call_floor))
        )
        
        suitable_elevators = [
            (abs(elevator.current_floor - call_floor), idx)
            for idx, elevator in enumerate(self.elevators)
            if is_suitable(elevator)
        ]
        suitable_elevators.sort()
        return suitable_elevators

    def transition(self, elevator, action):
        transitions = {
            ("IDLE", "MOVE_UP"): elevator.move_up,
            ("IDLE", "MOVE_DOWN"): elevator.move_down,
            ("MOVING", "MOVE_UP"): elevator.move_up,
            ("MOVING", "MOVE_DOWN"): elevator.move_down,
            ("MOVING", "OPEN_DOOR"): elevator.open_door,
            ("DOORS_OPEN", "CLOSE_DOOR"): elevator.close_door,
        }
        action_function = transitions.get((elevator.state, action))
        (action_function or (lambda: (_ for _ in ()).throw(Exception(f"Недопустимый переход: {elevator.state} -> {action}"))))()

    def process_call(self, call_floor, destination_floor):
        direction = (destination_floor > call_floor) * "up" + (destination_floor < call_floor) * "down"
        self.calls[call_floor][direction] = True

        best_elevators = self.find_best_elevator(call_floor, direction)
        (lambda: (_ for _ in ()).throw(Exception(f"Нет доступного лифта для вызова с этажа {call_floor}.")))() if not best_elevators else None

        best_elevator_idx = best_elevators[0][1]
        second_elevator_idx = best_elevators[1][1] if len(best_elevators) > 1 else best_elevator_idx

        best_elevator = self.elevators[best_elevator_idx]
        second_elevator = self.elevators[second_elevator_idx]

        elevator_to_use_idx = (abs(second_elevator.current_floor - call_floor) < abs(best_elevator.current_floor - call_floor)) * second_elevator_idx + \
                              (abs(second_elevator.current_floor - call_floor) >= abs(best_elevator.current_floor - call_floor)) * best_elevator_idx

        elevator = self.elevators[elevator_to_use_idx]
        elevator.add_task(call_floor)
        elevator.add_task(destination_floor)
        print(f"Вызов с этажа {call_floor} на этаж {destination_floor}. Назначен лифт №{elevator_to_use_idx + 1}.")

        while elevator.task_queue:
            next_floor = elevator.task_queue.pop(0)
            while elevator.current_floor != next_floor:
                action = (elevator.current_floor < next_floor) * "MOVE_UP" + (elevator.current_floor > next_floor) * "MOVE_DOWN"
                self.transition(elevator, action)

            self.transition(elevator, "OPEN_DOOR")
            self.transition(elevator, "CLOSE_DOOR")

        print(f"Лифт №{elevator_to_use_idx + 1} завершил задачи. Пройдено этажей: {elevator.steps}")
        print(f"Команды для лифта №{elevator_to_use_idx + 1}: {elevator.get_commands()}\n")
        elevator.reset_steps()


def main():
    num_floors = 10
    elevators_positions = [1, 5]
    controller = ElevatorController(num_floors, elevators_positions)

    calls = [(2, 8), (6, 1), (3, 7), (10, 2), (4, 5)]
    for call_floor, destination_floor in calls:
        controller.process_call(call_floor, destination_floor)

if __name__ == "__main__":
    main()
