





        
    # def test_rls_policy(self):
    #     """Test if RLS policy allows select, insert, update, and delete"""
    #     try:
            

    #         # 1. Test INSERT
    #         convo = {"user_id": self.get_user_id(), "messages": []}
    #         response = self.supabase.table("conversations").insert(convo).execute()
    #         insert_success = response.data and len(response.data) > 0
    #         convo_id = response.data[0]["id"] if insert_success else None
    #         print(f"{'✅' if insert_success else '❌'} Insert test")

    #         # Bail out if insert failed (can’t continue with select/update/delete)
    #         if not convo_id:
    #             return False

    #         # 2. Test SELECT
    #         response = (
    #             self.supabase
    #                 .table("conversations")
    #                 .select("id")
    #                 .limit(1)
    #                 .execute()
    #         )
    #         print(f"RLS select test successful: {len(response.data)} rows returned")

    #         # 3. Test UPDATE
    #         response = (
    #             self.supabase
    #                 .table("conversations")
    #                 .update({"messages": ["hello"]})
    #                 .eq("id", convo_id)
    #                 .execute()
    #         )
    #         update_success = response.data and response.data[0]["messages"] == ["hello"]
    #         print(f"{'✅' if update_success else '❌'} Update test")

    #         # 4. Test DELETE
    #         response = (
    #             self.supabase
    #                 .table("conversations")
    #                 .delete()
    #                 .eq("id", convo_id)
    #                 .execute()
    #         )
    #         delete_success = response.data and response.data[0]["id"] == convo_id
    #         print(f"{'✅' if delete_success else '❌'} Delete test")

    #         return insert_success and update_success and delete_success

    #     except Exception as e:
    #         print(f"RLS test failed: {e}")
    #         return False

    
