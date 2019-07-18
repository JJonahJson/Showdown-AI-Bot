import unittest
import src.protocol.request_parser as rp


class MyTestCase(unittest.TestCase):

    def test_something(self):
        text = """{
       "side":{
        "name":"errevas",
        "id":"p2",
        "pokemon":[
           {
              "ident":"p2: Sunflora",
              "details":"Sunflora, L89, M",
              "condition":"278/278",
              "active":true,
              "stats":{
                 "atk":138,
                 "def":149,
                "spa":238,
                "spd":202,
                "spe":104
             },
             "moves":[
                 "hiddenpowerfire60",
                "gigadrain",
                 "earthpower",
                "sunnyday"
             ],
             "baseAbility":"chlorophyll",
              "item":"lifeorb",
             "pokeball":"pokeball",
             "ability":"chlorophyll"
           }
            ]
        }
        }
        
        """

        field = rp.parse_and_set(text)
        self.assertEqual(field.active_pokemon_oppo.name, "Sunflora")


if __name__ == '__main__':
    unittest.main()
