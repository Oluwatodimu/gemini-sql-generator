CREATE TABLE app_user (
    id BINARY(16) NOT NULL UNIQUE,
    password_hash VARCHAR(64),
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    email VARCHAR(30) UNIQUE,
    phone_number VARCHAR(15) UNIQUE,
    image_url VARCHAR(256),
    activated BIT NOT NULL,
    user_type VARCHAR(11) NOT NULL,
    created_by VARCHAR(255),
    creation_date DATETIME,
    last_modified_by VARCHAR(255),
    last_modified_date DATETIME,

    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE authority (
    id BINARY(16) NOT NULL UNIQUE,
    authority_name VARCHAR(64) NOT NULL ,
    created_by VARCHAR(255),
    creation_date DATETIME,
    last_modified_by VARCHAR(255),
    last_modified_date DATETIME,

    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE user_authority (
    user_id BINARY(16) NOT NULL,
    authority_id BINARY(16) NOT NULL,

    PRIMARY KEY(user_id, authority_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE currency (
    `id` BINARY(16) NOT NULL UNIQUE,
    `name` VARCHAR(64) NOT NULL,
    `symbol` VARCHAR(30) NOT NULL UNIQUE,
    `enabled` BIT NOT NULL,
    created_by VARCHAR(255),
    creation_date DATETIME,
    last_modified_by VARCHAR(255),
    last_modified_date DATETIME,

    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE user_transaction (
    id BINARY(16) NOT NULL UNIQUE,
    amount DECIMAL(64) NOT NULL,
    `type` VARCHAR(15) NOT NULL,
    `purpose` VARCHAR(35) NOT NULL,
    `account_id` BINARY(16) NOT NULL,
    `reference` BINARY(16) NOT NULL UNIQUE,
    `status` VARCHAR(30) NOT NULL,
    `description` VARCHAR(255),
    `sender_account` VARCHAR(20) NOT NULL,
    `receiver_account` VARCHAR(20) NOT NULL,
    created_by VARCHAR(255),
    creation_date DATETIME,
    last_modified_by VARCHAR(255),
    last_modified_date DATETIME,

    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE account (
    id BINARY(16) NOT NULL UNIQUE,
    `available_balance` DECIMAL(64) NOT NULL,
    `reserved_balance` VARCHAR(30) NOT NULL,
    `locked` BIT NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    `type` VARCHAR(20) NOT NULL,
    `currency_id` BINARY(16) NOT NULL,
    `user_id` BINARY(16) NOT NULL,
    `account_number` VARCHAR(20) NOT NULL UNIQUE,
    created_by VARCHAR(255),
    creation_date DATETIME,
    last_modified_by VARCHAR(255),
    last_modified_date DATETIME,

    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;