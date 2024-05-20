CREATE TABLE contract_templates (
    id SERIAL PRIMARY KEY,
    ride_matching_service_endpoints TEXT,
    location_service_endpoints TEXT,
    notification_service_endpoints TEXT,
    trip_management_service_endpoints TEXT,
    ride_matching_service_contract_value DECIMAL(10, 2) NOT NULL,
    location_service_contract_value DECIMAL(10, 2) NOT NULL,
    notification_service_contract_value DECIMAL(10, 2) NOT NULL,
    trip_management_service_contract_value DECIMAL(10, 2) NOT NULL,
    total_contract_value DECIMAL(10, 2) NOT NULL CHECK (
        total_contract_value > (
            ride_matching_service_contract_value +
            location_service_contract_value +
            notification_service_contract_value +
            trip_management_service_contract_value
        )
    ),
    beneficiary_id INTEGER NOT NULL
);
