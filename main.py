    # try:
    #     employee = Employee.objects.get(
    #         slug="bohous-josef"
    #     )  # Najde zaměstnance podle slug
    #     face_vector_entry, created = (
    #         FaceVector.objects.update_or_create(
    #             employee=employee,  # Odkaz na zaměstnance
    #             defaults={
    #                 "face_vector": new_face_vector
    #             },  # Aktualizace sloupce face_vector
    #         )
    #     )
    #     if created:
    #         cons.log(
    #             "Nový FaceVector vytvořen pro 'bohous-josef'"
    #         )
    #     else:
    #         cons.log(
    #             "FaceVector aktualizován pro 'bohous-josef'"
    #         )

    # except Employee.DoesNotExist:
    #     cons.log(
    #         "Zaměstnanec 'bohous-josef' nebyl nalezen."
    #     )
