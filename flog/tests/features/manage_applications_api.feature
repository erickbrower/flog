Feature: Manage Logs via API
  In order to associate Log entries with the Host that created them
  As an end user (or Host client) of the API
  Use an API endpoint that allows management of Logs

  Scenario: Create a new Log entry for a Host with a signed request
    Given I have some Hosts
      | name               | instance     | api_key     | api_private_key | description | 
      | Test Application 1 | development  | test_1_dev  | private_key_1   | Testing...  | 
      | Test Application 1 | testing      | test_1_test | private_key_2   | Testing...  | 
      | Test Application 1 | production   | test_1_prod | private_key_3   | Testing...  | 

    When I send requests to create new Log entries
      | _api_key    | _timestamp | _signature | field1 | field2 | field3 | you_dont_have_to     |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | roxanne              |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | put_on_the_red_light |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | roxanne              |
      | test_1_dev  | GENERATE   | GENERATE   | foo    | bar    | baz    | put_on_the_red_light |
      | test_1_test | GENERATE   | GENERATE   | foo    | bar    | baz    | roxanne              |
      | test_1_prod | GENERATE   | GENERATE   | foo    | bar    | baz    | put_on_the_red_light |

    Then I should receive successful responses


  Scenario: Query for Logs by Host and field equality with a signed request
    Given I have some Hosts
      | name               | instance     | api_key     | api_private_key | description | 
      | Test Application 1 | development  | test_1_dev  | private_key_1   | Testing...  | 
      | Test Application 1 | testing      | test_1_test | private_key_2   | Testing...  | 
      | Test Application 1 | production   | test_1_prod | private_key_3   | Testing...  | 
    
    And I have some Logs
      | host_api_key    | field1 | field2 | field3 | hey_mickey  |
      | test_1_dev      | foo    | bar    | baz    | youre_so    |
      | test_1_dev      | foo    | bar    | baz    | fine        |
      | test_1_dev      | foo    | bar    | baz    | youre_so    |
      | test_1_dev      | foo    | bar    | baz    | fine        |

    When I send a request for all of 'test_1_dev' Logs with 'hey_mickey' = 'fine'
    Then I should get the two Logs in the response

