class Affiliate:
    def __init__(self, identification_type, identification_number, full_name,
                 current_income, desired_service, employment_modality,
                 affiliation_fee, affiliation_date):
        self.identification_type = identification_type
        self.identification_number = identification_number
        self.full_name = full_name
        self.current_income = current_income
        self.desired_service = desired_service
        self.employment_modality = employment_modality
        self.affiliation_fee = affiliation_fee
        self.affiliation_date = affiliation_date

    def __str__(self):
        return f"{self.full_name} - {self.identification_number}"