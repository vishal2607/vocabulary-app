export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_0jVsMXVBH',
      userPoolClientId: '3i06obe1h9mm2ltt7kn2b3c76a',
      signUpVerificationMethod: 'code',
      loginWith: {
        email: true,
      },
    },
  },
  API: {
    REST: {
      VocabularyAPI: {
        endpoint: 'https://rvqf004vc9.execute-api.us-east-1.amazonaws.com/Prod',
      },
    },
  },
};
