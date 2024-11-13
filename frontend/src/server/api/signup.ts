import { defineEventHandler, readBody } from "h3";

export default defineEventHandler(async (event) => {
  // Récupérer le corps de la requête (les données envoyées depuis le formulaire)
  const body = await readBody(event);

  // Désassembler les données du formulaire
  const { firstName, lastName, email, password, dob, address, acceptTerms } =
    body;

  // Valider les données (tu peux étendre la validation selon tes besoins)
  if (
    !firstName ||
    !lastName ||
    !email ||
    !password ||
    !dob ||
    !address ||
    !acceptTerms
  ) {
    return { statusCode: 400, message: "Tous les champs sont requis." };
  }

  // Simuler l'enregistrement dans la base de données
  // (ici, on va juste afficher les données dans la console pour l'instant)
  console.log("Nouveau utilisateur inscrit:", {
    firstName,
    lastName,
    email,
    dob,
    address,
  });

  // Retourner une réponse indiquant que l'inscription a réussi
  return {
    statusCode: 200,
    message: "Inscription réussie!",
    data: { firstName, lastName, email, dob, address },
  };
});
