from .data_structures import Stack, Queue, CustomList

class DataStructureManager:
    def __init__(self):
        self.stack = Stack()
        self.queue = Queue()
        self.list = CustomList()

    def add_affiliate(self, structure_name, affiliate):
        if structure_name == "Pila":
            self.stack.push(affiliate)
        elif structure_name == "Cola":
            self.queue.enqueue(affiliate)
        elif structure_name == "Lista":
            self.list.append(affiliate)
        else:
            raise ValueError(f"Estructura no válida: {structure_name}")

    def get_affiliates(self, structure_name):
        if structure_name == "Pila":
            return self.stack.get_all()
        elif structure_name == "Cola":
            return self.queue.get_all()
        elif structure_name == "Lista":
            return self.list.get_all()
        return []

    def get_report(self, structure_name):
        if structure_name == "Pila":
            # Suma de tarifas
            total = sum(a.affiliation_fee for a in self.stack.get_all())
            return f"Suma de tarifas: ${total:,.0f}"
        elif structure_name == "Cola":
            # Cantidad de registros
            return f"Cantidad de registros: {self.queue.size()}"
        elif structure_name == "Lista":
            # Promedio de ingresos actuales
            items = self.list.get_all()
            if not items:
                return "Promedio de ingresos: $0"
            avg = sum(a.current_income for a in items) / len(items)
            return f"Promedio de ingresos: ${avg:,.0f}"
        return ""

    def remove_affiliate(self, structure_name, identification_number=None):
        if structure_name == "Pila":
            if not self.stack.is_empty():
                self.stack.pop()
                return True
            return False
        elif structure_name == "Cola":
            if not self.queue.is_empty():
                self.queue.dequeue()
                return True
            return False
        elif structure_name == "Lista":
            if identification_number is not None:
                return self.list.remove_by_id(identification_number)
            return False
        return False