Feature: Manage Log Streams via API
  In order to associate Log entries with the Stream that created them
  As an end user (or Stream client) of the API
  Use an API endpoint that allows management of Logs

  Scenario: Create a new Log entry for a Stream with a signed request
    Given I have a Node
      | name        | domain_ip       | description     |  
      | Test Node 1 | erickbrower.org | This is a test. |
    
    And I have a Stream
      | name             | description | public_key | private_key | log_collection   |  
      | App Log Stream 1 | Testing...  | mickey     | mouse       | app_log_stream_1 |

    When I send requests to add new Log entries to the Stream 
      | walk   | you_dont_have_to     | _public_key | _timestamp | _signature |
      | hard   | roxanne              | mickey      |            |            |
      | softly | put_on_the_red_light | mickey      |            |            |
      | hard   | roxanne              | mickey      |            |            |
      | softly | put_on_the_red_light | mickey      |            |            |

    Then I should receive successful responses


  Scenario: Query for Logs by Stream and field equality with a signed request
    Given I have a Node
      | name        | domain_ip       | description     |  
      | Test Node 1 | erickbrower.org | This is a test. |
    
    And I have a Stream
      | name             | description | public_key | private_key | log_collection   |  
      | App Log Stream 1 | Testing...  | mickey     | mouse       | app_log_stream_1 |

    And I have some Logs
      | walk   | you_dont_have_to     |
      | hard   | roxanne              |          
      | softly | put_on_the_red_light | 
      | hard   | roxanne              | 
      | softly | put_on_the_red_light | 

    When I send a request for all of the Stream Logs with 'walk' = 'hard'
    Then I should get the two Logs in the response

