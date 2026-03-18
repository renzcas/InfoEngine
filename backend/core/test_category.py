from backend.core.infoengine_category import I, U, F, run_attack_pipeline

print("=== InfoEngine Category ===")
print(I)

print("\n=== CockpitUI Category ===")
print(U)

print("\n=== Functor F (Backend → UI) ===")
print(F)

print("\n=== Pipeline Output ===")
result = run_attack_pipeline({"scenario": "SQLi"})
print(result)
