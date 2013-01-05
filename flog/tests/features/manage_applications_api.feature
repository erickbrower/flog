Feature: Manage Logs via API
  In order to associate Log entries with the Host that created them
  As an end user (or Host client) of the API
  Use an API endpoint that allows management of Logs

  Scenario: Create a new Log entry for a Host with a signed request
    Given I have a User account
      | email_address | password_hash |
      | test@test.com | 12345678      |
    
    And I have a Host 
      | name               | description | 
      | Test Application 1 | Testing...  | 

    And my User KeyRing has a Key to the Host 'Test Application 1'
      | public_key | private_key |
      | user_key_1 | d0ntp4nic   |

    When I send requests to create new Log entries for the Host
      | _public_key | field1 | field2 | field3 | you_dont_have_to     | _timestamp | _signature |
      | user_key_1  | foo    | bar    | baz    | roxanne              |            |            |
      | user_key_1  | foo    | bar    | baz    | put_on_the_red_light |            |            |
      | user_key_1  | foo    | bar    | baz    | roxanne              |            |            |
      | user_key_1  | foo    | bar    | baz    | put_on_the_red_light |            |            |
      | user_key_1  | foo    | bar    | baz    | roxanne              |            |            |
      | user_key_1  | foo    | bar    | baz    | put_on_the_red_light |            |            |

    Then I should receive successful responses


  Scenario: Query for Logs by Host and field equality with a signed request
    Given I have a User account
      | email_address | password_hash |
      | test@test.com | 12345678      |
    
    And I have a Host 
      | name               | description | 
      | Test Application 1 | Testing...  | 

    And my User KeyRing has a Key to the Host
      | public_key | private_key |
      | user_key_1 | d0ntp4nic   |

    And I have some Logs
      | field1 | field2 | field3 | hey_mickey  |
      | foo    | bar    | baz    | youre_so    |
      | foo    | bar    | baz    | fine        |
      | foo    | bar    | baz    | youre_so    |
      | foo    | bar    | baz    | fine        |

    When I send a request for all of the Host Logs with 'hey_mickey' = 'fine'
    Then I should get the two Logs in the response

