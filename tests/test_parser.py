from numjuggler.parser import Card


class TestCardParser:
    def test_vol_param(self):
        definition = [
            "600177 400 -1.00000e+00 $ WATER_LEFT\n",
            "          600003 -600421 601230 -600013 600011\n",
            "           Vol=1.335972e+01\n",
            "           imp:n=1.0   imp:p=1.0   U=5972  \n",
        ]

        cell2 = Card(definition, ctype=3, pos=1)
        cell2.get_values()

        cell2._set_value_by_type("u", 30)
        assert "U=30" in cell2.card()
        assert "Vol=1.335972e+01" in cell2.card()
