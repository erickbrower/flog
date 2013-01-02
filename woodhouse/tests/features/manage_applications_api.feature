Feature: Creating Logs via API
  In order to associate Log entries with the Host that created them
  As an end user (or Host client) of the API
  Use an API endpoint that allows management of Logs

  Scenario: Create a new Log entry for a Host with a signed request
    Given I have some valid Hosts
      | name               | instance     | api_key     | api_private_key | description | 
      | Test Application 1 | development  | test_1_dev  | private_key_1   | Testing...  | 
      | Test Application 1 | testing      | test_1_test | private_key_2   | Testing...  | 
      | Test Application 1 | production   | test_1_prod | private_key_3   | Testing...  | 

    When I send requests to create new Log entries
      | _api_key    | _timestamp | _signature | field1 | field2 | field3 | hey_mickey  |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | youre_so    |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | fine        |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | youre_so    |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | fine        |
      | test_1_test | GENERATE   | GENERATE   | foo    | bar    | baz    | you_blow_my |
      | test_1_prod | GENERATE   | GENERATE   | foo    | bar    | baz    | mind        | 

    Then I should be able to query for the Logs
      | _api_key    |
      | test_1_dev  |
      | test_1_test |
      | test_1_prod |
