import streamlit as st


def main():
    st.title("APBA Rating Demo")

    st.image("assets/apba_image.gif", use_column_width=True)

    st.write("On this page, you can interact with the the tools available to view APBA ratings and compare them to "
             "the generated ones")

    st.write('To view the different ratings pages view th columns on the sidebar')




if __name__ == '__main__':
    main()
